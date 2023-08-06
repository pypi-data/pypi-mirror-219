# AWS EC2 Instance Connect Custom Resource

AWS EC2 instance connect custom resource

## Resources

This construct creating resource list.

* AWS Custom Resource

  * Lambda Function Iam Role
  * Lambda Function
  * Custom Resource Iam Role
  * Custom Policy

## Install

### TypeScript

```shell
npm install @gammarer/aws-ec2-instance-connect-custom-resource
# or
yarn add @gammarer/aws-ec2-instance-connect-custom-resource
```

### Python

```shell
pip install gammarer.aws-ec2-instance-connect-custom-resource
```

## Example

```shell
npm install @gammarer/aws-ec2-instance-connect-custom-resource
```

```python
import { EC2InstanceConnectCustomResource } from '@gammarer/aws-ec2-instance-connect-custom-resource';

new EC2InstanceConnectCustomResource(stack, 'EC2InstanceConnectCustomResource', {
  subnetId: 'example-subnet-id',
  securityGroupIds: [
    'example-security-group-id',
  ],
});
```

## License

This project is licensed under the Apache-2.0 License.
