# Deployment & Configuration Guide

This guide documents how to build, configure, and deploy the DocInsight API using the Serverless Framework.

## Prerequisites

### System Requirements

- Python 3.11+
- Docker (for ECR image building and LocalStack)
- AWS Account with appropriate IAM permissions
- Git

### AWS Resources Required

- ECR repository (for Docker images)
- S3 bucket for CloudFormation artifacts
- IAM role with Lambda, DynamoDB, S3, Textract, EventBridge, SNS, SQS permissions
- VPC with subnets for Redis/Neon database access (optional but recommended)

### Environment Variables

Create a `.env.local` file with these values (never commit to version control):

```bash
# AWS Configuration
AWS_REGION=us-east-1
AWS_PROFILE=default

# Deployment
ECR_IMAGE_URI=<aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/docinsight:latest
LAMBDA_SECURITY_GROUP_ID=sg-xxxxxxxxx
SUBNET_ID=subnet-xxxxxxxxx
SUBNET2_ID=subnet-yyyyyyyyy

# JWT Configuration
JWT_PRIVATE_KEY=-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----
JWT_PUBLIC_KEY=-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----

# OpenAI
OPENAI_API_KEY=sk-...

# Database (Neon PostgreSQL + pgvector)
NEON_DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Redis
REDIS_HOST=redis.example.com
REDIS_PORT=6379
REDIS_PASSWORD=<optional>
```

## Building & Pushing Docker Image

### Step 1: Build Docker Image

```bash
docker build -t docinsight:latest .
```

This Dockerfile:

- Uses AWS Lambda Python 3.11 base image
- Installs dependencies from requirements.txt
- Copies source code to Lambda task root

### Step 2: Authenticate with ECR

```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
```

### Step 3: Tag and Push Image

```bash
docker tag docinsight:latest <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/docinsight:latest
docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/docinsight:latest
```

### Step 4: Update ECR_IMAGE_URI

```bash
export ECR_IMAGE_URI=<aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/docinsight:latest
```

## Deployment with Serverless Framework

### Step 1: Install Serverless Framework

```bash
npm install -g serverless
npm install serverless-python-requirements --save-dev
```

### Step 2: Deploy Stack

```bash
# Development environment
serverless deploy --stage dev

# Production environment
serverless deploy --stage prod
```

### Step 3: Review Deployment

```bash
serverless info --stage dev
```

Output will show:

```
Service Information
service: document-analyzer-api
stage: dev
region: us-east-1
stack: document-analyzer-api-dev
resources: XX
api keys:
  None
endpoints:
  POST - https://xxx.execute-api.us-east-1.amazonaws.com/document
  POST - https://xxx.execute-api.us-east-1.amazonaws.com/signin
  POST - https://xxx.execute-api.us-east-1.amazonaws.com/signup
  POST - https://xxx.execute-api.us-east-1.amazonaws.com/chat
  GET - https://xxx.execute-api.us-east-1.amazonaws.com/messages/{conversation_id}
  wss://xxx.execute-api.us-east-1.amazonaws.com/dev
functions:
  createDocument: document-analyzer-api-dev-createDocument
  signin: document-analyzer-api-dev-signin
  signup: document-analyzer-api-dev-signup
  startExtracting: document-analyzer-api-dev-startExtracting
  indexDocument: document-analyzer-api-dev-indexDocument
  textractCompleted: document-analyzer-api-dev-textractCompleted
  askQuestion: document-analyzer-api-dev-askQuestion
  questionProcessing: document-analyzer-api-dev-questionProcessing
  processQuestion: document-analyzer-api-dev-processQuestion
  updateCache: document-analyzer-api-dev-updateCache
  getMessages: document-analyzer-api-dev-getMessages
  websocketConnect: document-analyzer-api-dev-websocketConnect
  websocketDisconnect: document-analyzer-api-dev-websocketDisconnect
  websocketPostToConnection: document-analyzer-api-dev-websocketPostToConnection
```

## Configuration Reference

### serverless.yml Structure

#### Provider Configuration

```yaml
provider:
  name: aws
  region: us-east-1
  runtime: python3.11
  architecture: x86_64
  environment:
    # Environment variables passed to all Lambda functions
    BUCKET_NAME: !Ref UploadsBucket
    DOCUMENT_TABLE: !Ref DocumentTable
    # ... more variables from .env

  iam:
    role:
      statements:
        # S3 permissions for document upload/retrieval
        - Effect: Allow
          Action: [s3:PutObject, s3:GetObject]
          Resource: "${UploadsBucket.Arn}/*"

        # DynamoDB permissions for all tables
        - Effect: Allow
          Action: [dynamodb:Query, dynamodb:Scan, dynamodb:GetItem, ...]
          Resource:
            - !GetAtt DocumentTable.Arn
            - !Sub "${DocumentTable.Arn}/index/*"
            # ... other table ARNs

        # Textract permissions for document analysis
        - Effect: Allow
          Action: [textract:StartDocumentAnalysis, textract:GetDocumentAnalysis]
          Resource: "*"

        # EventBridge permissions for event publishing
        - Effect: Allow
          Action: events:PutEvents
          Resource: "arn:aws:events:us-east-1:*:event-bus/default"

        # SQS permissions for question queue
        - Effect: Allow
          Action: sqs:SendMessage
          Resource: !GetAtt QuestionsQueue.Arn
```

#### Functions Configuration

**HTTP API Functions (No VPC):**

- `createDocument` - POST /document
- `signin` - POST /signin
- `signup` - POST /signup
- `askQuestion` - POST /chat
- `getMessages` - GET /messages/{conversation_id}

**Event-Driven Functions (No VPC):**

- `startExtracting` - S3 EventBridge trigger
- `indexDocument` - S3 EventBridge trigger
- `textractCompleted` - SNS trigger
- `websocketConnect` - WebSocket $connect
- `websocketDisconnect` - WebSocket $disconnect
- `websocketPostToConnection` - EventBridge trigger

**Event-Driven Functions (With VPC):**

- `questionProcessing` - EventBridge trigger (requires VPC for Redis/Neon)
- `updateCache` - EventBridge trigger (requires VPC for Redis)
- `processQuestion` - SQS trigger (requires VPC for Neon)

**VPC Configuration (when needed):**

```yaml
functions:
  questionProcessing:
    vpc:
      securityGroupIds:
        - ${env:LAMBDA_SECURITY_GROUP_ID}
      subnetIds:
        - ${env:SUBNET_ID}
        - ${env:SUBNET2_ID}
    timeout: 15
```

#### Resources Configuration

**S3 Bucket:**

```yaml
UploadsBucket:
  Type: AWS::S3::Bucket
  Properties:
    BucketName: docinsight-raw-documents
    NotificationConfiguration:
      EventBridgeConfiguration:
        EventBridgeEnabled: true # Auto-route all S3 events to EventBridge
```

**DynamoDB Tables (5 total, all on-demand):**

- `document-table` - Document metadata (PK: id, GSI: s3_key, textract_job_id, extracted_text_key)
- `user-table` - User identity (PK: id, GSI: email)
- `chat-table` - Chat messages (PK: id, GSI: conversation_id, document_id)
- `conversation-table` - Conversations (PK: id, GSI: document_id)
- `connection-table` - WebSocket connections (PK: connection_id, GSI: user_id)

**SNS Topic & Subscription:**

```yaml
TextractTopic:
  Type: AWS::SNS::Topic
  Properties:
    TopicName: textract-document-completed

TextractSubscription:
  Type: AWS::SNS::Subscription
  Properties:
    TopicArn: !Ref TextractTopic
    Protocol: lambda
    Endpoint: !GetAtt TextractCompletedLambdaFunction.Arn
```

**SQS Queues:**

```yaml
QuestionsQueue:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: question-queue-service
    VisibilityTimeout: 60
    RedrivePolicy:
      maxReceiveCount: 3
      deadLetterTargetArn: !GetAtt QuestionsDLQ.Arn

QuestionsDLQ:
  Type: AWS::SQS::Queue
  Properties:
    QueueName: questions-queue-dlq-service
```

## Local Development

### Using LocalStack

1. **Start LocalStack with Docker Compose:**

   ```bash
   docker-compose -f docker-compose.localstack.yml up -d
   ```

2. **Deploy to LocalStack:**

   ```bash
   serverless deploy --stage local
   ```

3. **Run tests against local services:**
   ```bash
   pytest tests/ --local
   ```

### Using serverless-offline Plugin

1. **Install plugin:**

   ```bash
   npm install serverless-offline --save-dev
   ```

2. **Start offline mode:**
   ```bash
   serverless offline start
   ```

## Monitoring & Observability

### CloudWatch Logs

All Lambda functions automatically log to CloudWatch under:

```
/aws/lambda/document-analyzer-api-<stage>-<function-name>
```

### CloudWatch Metrics

Monitor:

- Lambda invocations, duration, errors
- DynamoDB read/write capacity, throttles
- S3 request count
- Textract job status
- EventBridge rule matches
- SQS queue depth

### Custom Metrics

Add custom metrics in Lambda functions:

```python
from aws_lambda_powertools import Metrics

metrics = Metrics()
metrics.add_metric(name="DocumentProcessed", unit="Count", value=1)
metrics.flush()
```

## Security Considerations

### IAM Least Privilege

- Each function has only required permissions
- S3 access scoped to specific bucket ARNs
- DynamoDB access scoped to specific table ARNs

### Encryption

- S3 bucket encryption at rest (default AWS managed)
- DynamoDB encryption (default AWS managed)
- In-transit: HTTPS for API Gateway, encrypted SNS/SQS

### API Security

- JWT token validation on all HTTP endpoints
- Authorization context extracted from JWT claims
- Access control via user_id matching

### Secrets Management

- Use AWS Secrets Manager for sensitive values
- Avoid hardcoding secrets in serverless.yml
- Rotate JWT keys regularly

## Troubleshooting

### Lambda Function Errors

**Cold start timeout:**

- Increase timeout in serverless.yml
- Consider reducing package size
- Pre-warm Lambda if needed

**Permission denied errors:**

- Verify IAM statements in serverless.yml
- Check resource ARNs (especially GSI arns for DynamoDB)

### EventBridge Issues

**Events not triggering:**

- Verify S3 bucket has EventBridge notifications enabled
- Check EventBridge rule patterns match event structure
- Verify target Lambda has invoke permission

**SNS subscription not firing:**

- Check TextractPermission resource exists
- Verify SNS topic ARN in Textract role

### Database Issues

**DynamoDB throttling:**

- Switch to provisioned capacity if needed
- Review query patterns for table scans
- Add appropriate GSIs for query patterns

**Connection timeouts:**

- Verify VPC configuration (security group, subnets)
- Check NAT gateway for external API calls
- Verify database credentials in environment

## Cost Optimization

### Recommended Settings

```yaml
# DynamoDB
BillingMode: PAY_PER_REQUEST # Auto-scales, no provisioning

# Lambda
timeout: 15 # Keep reasonable to avoid unnecessary costs
memory: 128 # Default is good for most operations

# S3
LifecyclePolicy: # Archive old documents
  Transitions:
    - TransitionInDays: 90
      StorageClass: GLACIER
```

### Cost Monitoring

1. Set up AWS Budgets alerts
2. Monitor CloudWatch metrics for unusual patterns
3. Review Lambda duration trends
4. Track Textract job counts and OpenAI API usage

## Deployment Checklist

Before deploying to production:

- [ ] All environment variables set in AWS Systems Manager Parameter Store
- [ ] JWT keys rotated and stored securely
- [ ] DynamoDB backups configured
- [ ] S3 bucket versioning enabled
- [ ] EventBridge rule patterns tested
- [ ] Lambda timeouts reviewed
- [ ] IAM permissions audited
- [ ] Error handling tested
- [ ] Monitoring and alarms configured
- [ ] Load tested with expected traffic volume
