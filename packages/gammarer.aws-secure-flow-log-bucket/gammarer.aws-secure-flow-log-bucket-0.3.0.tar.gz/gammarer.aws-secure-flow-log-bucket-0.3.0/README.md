# AWS Secure Flow Log Bucket

Specific AWS VPC FlowLog Bucket

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-flow-log-bucket
# or
yarn add @gammarer/aws-secure-flow-log-bucket
```

### Python

```shell
pip install gammarer.aws-secure-flow-log-bucket
```

## Example

### TypeScript

```shell
npm install @gammarer/aws-secure-flow-log-bucket
```

```python
import { SecureFlowLogBucket } from '@gammarer/aws-secure-flow-log-bucket';

const bucket = new SecureFlowLogBucket(stack, 'SecureFlowLogBucket', {
  keyPrefixes: [
    'example-prefix-a',
    'example-prefix-b',
  ],
});
```

## License

This project is licensed under the Apache-2.0 License.
