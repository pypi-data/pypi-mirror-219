import React, { FC, useState, SyntheticEvent } from 'react';
import { Grid } from 'react-loader-spinner';
import { resumeClusterHandler } from './handler';
import { ClusterStatus, ICluster } from './types';

interface IOptionProps {
  cluster: ICluster;
  current?: boolean;
  callback?: any;
  forceUpdate?: () => void;
}

export const RunningClusterSelectOption: FC<IOptionProps> = ({
  cluster,
  current = false,
  callback,
}: IOptionProps) => {
  return (
    <div
      className={`${current ? 'current-cluster-option' : ''} bodo-cluster-dropdown-item`}
      onClick={!current ? () => callback(cluster.uuid) : () => true}
      key={cluster.uuid}
    >
      <div>
        <span className="cluster-name">{cluster.name}</span>
        <span className="cluster-details">Bodo {cluster.bodoVersion}</span>
      </div>
      {current && <button onClick={() => callback()}>Detach</button>}
    </div>
  );
};

export const NonRunningClusterSelectOption: FC<IOptionProps> = ({
  cluster,
  forceUpdate,
}: IOptionProps) => {
  const [isProcessing, setProcessing] = useState(false);
  const startLoading = () => {
    setProcessing(true);
    setTimeout(() => setProcessing(false), 5000);
  };
  const resumeCluster = (cluster_uuid: string) => async (e: SyntheticEvent) => {
    if (!confirm('Are you sure that you want to resume this cluster')) {
      return false;
    }
    await resumeClusterHandler(cluster_uuid);
    if (forceUpdate) {
      // Force Update is ran to update the visual state.
      forceUpdate();
    }
    startLoading();
  };

  return (
    <div className={`bodo-cluster-dropdown-item paused-bodo-clusuter`} key={cluster.uuid}>
      <div>
        <span className="cluster-name">{cluster.name}</span>
        <span className="cluster-details">Bodo {cluster.bodoVersion}</span>
      </div>
      {cluster.status !== ClusterStatus.PAUSED || isProcessing ? (
        <div className="cluster-select-resume-loading">
          <Grid ariaLabel="loading-indicator" width={10} height={10} />
        </div>
      ) : (
        <div className="cluster-select-resume-cluster" onClick={resumeCluster(cluster.uuid)}>
          <svg
            width="35"
            height="47"
            viewBox="0 0 35 47"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M33.992 25.435C34.3029 25.2194 34.5571 24.9309 34.7327 24.5944C34.9083 24.2579 35 23.8834 35 23.5032C35 23.123 34.9083 22.7485 34.7327 22.412C34.5571 22.0754 34.3029 21.7869 33.992 21.5713L3.66075 0.419678C3.3109 0.174847 2.90114 0.0312738 2.47598 0.00455464C2.05081 -0.0221645 1.62651 0.0689923 1.24916 0.268124C0.871822 0.467255 0.555873 0.766742 0.335644 1.13405C0.115415 1.50135 -0.000670061 1.92243 9.40679e-07 2.35153L2.78982e-06 44.6548C0.00175831 45.0829 0.119337 45.5025 0.340093 45.8683C0.560849 46.2341 0.876431 46.5324 1.2529 46.7311C1.62937 46.9297 2.05248 47.0213 2.47674 46.9958C2.90099 46.9704 3.31034 46.8289 3.66075 46.5867L33.992 25.435Z"
              fill="#5E5E5E"
            />
          </svg>
        </div>
      )}
    </div>
  );
};
