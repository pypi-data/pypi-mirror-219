# AWS RDS Database Running Scheduler

This is an AWS CDK Construct to make RDS Database running schedule (only running while working hours(start/stop)).

## Fixed

* RDS Aurora Cluster
* RDS Instance

## Resources

This construct creating resource list.

* EventBridge Scheduler execution role
* EventBridge Scheduler

## Install

### TypeScript

```shell
npm install @gammarer/aws-rds-database-running-scheduler
# or
yarn add @gammarer/aws-rds-database-running-scheduler
```

### Python

```shell
pip install gammarer.aws-rds-database-running-scheduler
```

## Example

```shell
npm install @gammarer/aws-rds-database-running-scheduler
```

```python
import { RdsDatabaseRunningScheduler, Type } from '@gammarer/aws-rds-database-running-scheduler';

new RdsDatabaseRunningScheduler(stack, 'RdsDatabaseRunningScheduler', {
  type: Type.CLUSTER, // TYPE.CLUSTER or TYPE.INSTANCE
  identifiers: {
    ['db-cluster-1a']: { // cluster identirier
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
  },
})
```

## License

This project is licensed under the Apache-2.0 License.
