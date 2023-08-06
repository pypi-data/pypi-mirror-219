# AWS EC2 AutoScaling Instance Running Scheduler

This is an AWS CDK Construct to make EC2 AutoScaling instance running schedule (only running while working hours(start/stop)).
But only capacity min value is 0 for the AutoScalingGroup.

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarer/aws-ec2-auto-scaling-instance-running-scheduler
# or
yarn add @gammarer/aws-ec2-auto-scaling-instance-running-scheduler
```

### Python

```shell
pip install gammarer.aws-ec2-auto-scaling-instance-running-scheduler
```

## Example

```shell
npm install @gammarer/aws-ec2-auto-scaling-instance-running-scheduler
```

```python
import { Ec2AutoScalingInstanceRunningScheduler } from '@gammarer/aws-ec2-auto-scaling-instance-running-scheduler';

new Ec2AutoScalingInstanceRunningScheduler(stack, 'Ec2AutoScalingInstanceRunningScheduler', {
  targets: [
    {
      groupName: 'example-scaling-group',
      runningDesiredCapacity: 2,
      startSchedule: {
        timezone: 'UTC',
      },
      stopSchedule: {
        timezone: 'UTC',
      },
    },
  ],
});
```

## License

This project is licensed under the Apache-2.0 License.
