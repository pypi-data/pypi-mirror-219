import React, { FC, useRef, useState } from 'react';
import { Grid } from 'react-loader-spinner';
import { NonRunningClusterSelectOption, RunningClusterSelectOption } from './clusterSelectOption';
import { ClusterStore } from './store';
import { ClusterStatus, ICluster } from './types';
import { compareStatus } from './utils';

export const ChevronSVG: FC = () => (
  <svg
    height="20"
    className="bodo-select-chevron"
    width="20"
    viewBox="0 0 20 20"
    aria-hidden="true"
    focusable="false"
  >
    <path d="M4.516 7.548c0.436-0.446 1.043-0.481 1.576 0l3.908 3.747 3.908-3.747c0.533-0.481 1.141-0.446 1.574 0 0.436 0.445 0.408 1.197 0 1.615-0.406 0.418-4.695 4.502-4.695 4.502-0.217 0.223-0.502 0.335-0.787 0.335s-0.57-0.112-0.789-0.335c0 0-4.287-4.084-4.695-4.502s-0.436-1.17 0-1.615z"></path>
  </svg>
);

interface ITriggerProps {
  cluster: ICluster | null;
  isProcessing: boolean;
}

const ClusterSelectTrigger: FC<ITriggerProps> = ({ cluster, isProcessing }: ITriggerProps) => {
  return (
    <>
      <div className="bodo-currently-selected-dropdown">
        {isProcessing ? (
          <div
            style={{
              width: '100%',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <span>Loading...</span>
            <span>
              <Grid ariaLabel="loading-indicator" width={10} height={10} />
            </span>
          </div>
        ) : (
          <>
            <span>{cluster ? cluster.name : 'Detached'}</span>
            <ChevronSVG />
          </>
        )}
      </div>
    </>
  );
};

interface IClusterSelectProps {
  currentClusterUUID?: string | undefined | null;
  clusters: any[];
  myOnChange: any;
  clusterAttachloading: boolean;
  store: ClusterStore;
}

const ClusterSelectList: FC<IClusterSelectProps> = ({
  currentClusterUUID,
  myOnChange,
  clusters,
  clusterAttachloading,
  store,
}: IClusterSelectProps) => {
  const [isSelecting, setIsSelecting] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const ref = useRef(null);
  const clusterFromUUID = (uuid: string | undefined | null) => {
    return clusters.find((cluster) => cluster.uuid === uuid);
  };
  const renderOptions = () => {
    const currentCluster = clusterFromUUID(currentClusterUUID);
    const renderedClusters = clusters
      .filter((cluster) => cluster.status !== ClusterStatus.NEW)
      .sort(compareStatus);
    return renderedClusters
      .filter((option) => {
        if (currentCluster) {
          return currentClusterUUID !== option.uuid;
        }
        return true;
      })
      .map((option) =>
        option.status === ClusterStatus.RUNNING ? (
          <RunningClusterSelectOption cluster={option} callback={handleSelect} />
        ) : (
          <NonRunningClusterSelectOption forceUpdate={() => store.forceUpdate()} cluster={option} />
        )
      );
  };

  const handleAttachDetach = (uuid: string, detach?: boolean) => {
    setIsProcessing(true);
    myOnChange(detach ? '0' : uuid);
    // We add a timeout to make the loading more natural
    setTimeout(() => {
      setIsProcessing(false);
    }, 1000);
    setIsSelecting(false);
  };

  const handleSelect = (uuid: string) => {
    handleAttachDetach(uuid, false);
  };
  const handleDetach = (uuid: string) => {
    handleAttachDetach(uuid, true);
  };

  const currentCluster = clusterFromUUID(currentClusterUUID);
  const handleToggle = () => {
    setIsSelecting(!isSelecting);
  };
  const { current: lastCluster }: any = ref;
  // If a cluster has been selected and it's not running then the cluster will detach, we keep track
  // of this by comparing the ref from the last render and the current cluster.
  if (
    lastCluster &&
    lastCluster.status === ClusterStatus.RUNNING &&
    (!currentCluster || currentCluster.status !== ClusterStatus.RUNNING)
  ) {
    handleDetach('0');
  }
  ref.current = currentCluster;

  return (
    <>
      <div className="bodo-dropdown-container">
        <div onClick={handleToggle}>
          <ClusterSelectTrigger
            cluster={currentClusterUUID ? clusterFromUUID(currentClusterUUID) : null}
            isProcessing={isProcessing || clusterAttachloading}
          />
        </div>
        <div className={`bodo-dropdown-list ${isSelecting ? 'selecting' : ''}`}>
          {clusters.length === 0 ? (
            <div className="bodo-dropdown-item">
              <div>
                <span className="cluster-name">No Clusters Available</span>
              </div>
            </div>
          ) : (
            <>
              {currentCluster ? (
                <>
                  <div className="bodo-drop-down-details">Attached Cluster:</div>
                  <RunningClusterSelectOption
                    cluster={currentCluster}
                    current={true}
                    callback={handleDetach}
                  />
                  <div className="bodo-drop-down-details">Detach & Attach:</div>
                </>
              ) : (
                <div className="bodo-drop-down-details">Attach:</div>
              )}
              {renderOptions()}
            </>
          )}
        </div>
      </div>
    </>
  );
};

export default ClusterSelectList;
