# AWS Secure Bucket

This is a Simple S3 Secure Bucket.

* Bucket Access Control is Private
* Public Read Access is false
* Enforce SSL
* All Block public access
* Require encryption

## Install

### TypeScript

```shell
npm install aws-secure-bucket
```

or

```shell
yarn add aws-secure-bucket
```

### Python

```shell
pip install aws-secure-bucket
```

## Example

### TypeScript

```shell
npm install aws-secure-bucket
```

```python
import { SecureBucket } from 'aws-secure-bucket';

const bucket = new SecureBucket(stack, 'SecureBucket', {
  bucketName: 'example-secure-bucket',
});
```
