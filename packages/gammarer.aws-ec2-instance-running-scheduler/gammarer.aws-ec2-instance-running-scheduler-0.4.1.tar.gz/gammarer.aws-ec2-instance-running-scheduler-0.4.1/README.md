# AWS EC2 Instance Running Scheduler

This is an AWS CDK Construct to make EC2 instance running schedule (only running while working hours(start/stop)).

## Fixed

* EC2 Instance

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarer/aws-ec2-instance-running-scheduler
# or
yarn add @gammarer/aws-ec2-instance-running-scheduler
```

### Python

```shell
pip install gammarer.aws-ec2-instance-running-scheduler
```

## Example

```shell
npm install @gammarer/aws-ec2-instance-running-scheduler
```

```python
import { Ec2InstanceRunningScheduler } from '@gammarer/aws-ec2-instance-running-scheduler';

new Ec2InstanceRunningScheduler(stack, 'Ec2InstanceRunningScheduler', {
  targets: [
    {
      instances: ['i-0af01c0123456789a', 'i-0af01c0123456789b'],
      startSchedule: {
        timezone: 'Asia/Tokyo',
        minute: '55',
        hour: '8',
        week: 'MON-FRI',
      },
      stopSchedule: {
        timezone: 'Asia/Tokyo',
        minute: '5',
        hour: '19',
        week: 'MON-FRI',
      },
    },
  ],
});
```

## License

This project is licensed under the Apache-2.0 License.
