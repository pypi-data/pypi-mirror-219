import { ClusterStatus, ICluster } from './types';

export function compareStatus(clusterA: ICluster, clusterB: ICluster): number {
  if (clusterA.status === clusterB.status) {
    return 0;
  }
  if (clusterA.status === ClusterStatus.RUNNING) {
    return -1;
  }
  if (clusterB.status === ClusterStatus.RUNNING) {
    return 1;
  }
  if (clusterA.status === ClusterStatus.INITIALIZING) {
    return -1;
  }
  if (clusterB.status === ClusterStatus.INITIALIZING) {
    return 1;
  }
  return 0;
}
