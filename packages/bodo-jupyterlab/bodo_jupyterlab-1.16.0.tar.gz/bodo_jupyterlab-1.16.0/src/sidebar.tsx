import * as React from 'react';
import { IChangedArgs } from '@jupyterlab/coreutils';
import { ClusterStore } from './store';
import { ReactWidget } from '@jupyterlab/apputils';
import ClusterResumePause from './resumePauseButton';
import { ClusterStatus, ICluster } from './types';
import ClusterStatusComponent from './clusterStatus';
import ClusterTerminalButton from './clusterTerminal/clusterTerminalButton';
import { JupyterFrontEnd } from '@jupyterlab/application';
import { compareStatus } from './utils';
import ClusterStopRestart from './stopRestartButton';
import { Grid } from 'react-loader-spinner';

interface IClusterListingItemProps {
  cluster: ICluster;
  forceUpdate: () => void;
  app: JupyterFrontEnd;
}
function ClusterListItem(props: IClusterListingItemProps) {
  const { cluster, forceUpdate, app } = props;
  const itemClass = 'bodo-ClusterListingItem';
  const [loadingType, setLoadingType] = React.useState<string>('');

  const startLoading = (loadType: string) => {
    setLoadingType(loadType);
    setTimeout(() => {
      setLoadingType('');
    }, 5000);
  };
  return (
    <li className={itemClass} data-cluster-id={cluster.uuid} key={cluster.uuid}>
      <div className="bodo-ClusterListingItem-title">{cluster.name}</div>
      <div>{cluster.uuid}</div>

      <div className="bodo-ClusterListingItem-stats">
        <span className="bodo-ClusterListingItem-stats-name">Instances:</span>{' '}
        {cluster.workersQuantity}
      </div>
      <div className="bodo-ClusterListingItem-stats">
        <span className="bodo-ClusterListingItem-stats-name">Instance Type:</span>{' '}
        {cluster.instanceType}
      </div>
      <div className="bodo-ClusterListingItem-stats">
        <span className="bodo-ClusterListingItem-stats-name">Bodo Version:</span>{' '}
        {cluster.bodoVersion}
      </div>
      {/* <div className="bodo-ClusterListingItem-stats">
        <span className="bodo-ClusterListingItem-stats-name">Cluster ID:</span> {cluster.uuid}
      </div> */}
      <div className="bodo-ClusterListingItem-status-and-buttons">
        <div className="bodo-ClusterListingItem-stats">
          <span className="bodo-ClusterListingItem-stats-name">Status:</span>{' '}
          <ClusterStatusComponent status={loadingType ? loadingType : cluster.status} />
        </div>
        <div className="bodo-ClusterListingItem-buttons">
          {![
            ClusterStatus.INPROGRESS,
            ClusterStatus.PAUSING,
            ClusterStatus.RESUMING,
            ClusterStatus.STOPPING,
            ClusterStatus.TERMINATING,
          ].includes(cluster.status) ? (
            <>
              <ClusterTerminalButton app={app} cluster={cluster} />
              <ClusterResumePause
                forceUpdate={() => forceUpdate()}
                startLoading={startLoading}
                uuid={cluster.uuid}
                clusterStatus={cluster.status}
              />
              <ClusterStopRestart
                clusterStatus={cluster.status}
                uuid={cluster.uuid}
                startLoading={startLoading}
                forceUpdate={() => forceUpdate()}
              />
            </>
          ) : (
            <span>
              <Grid ariaLabel="loading-indicator" width={10} height={10} />
            </span>
          )}
        </div>
      </div>
    </li>
  );
}

function EmptyClustersList(props: any) {
  const itemClass = 'bodo-ClusterListingItem';

  return (
    <li className={itemClass}>
      <div className="bodo-ClusterListingItem-title">No Clusters</div>
    </li>
  );
}

interface IClusterListProps {
  store: ClusterStore;
  app: JupyterFrontEnd;
}
interface IClusterListState {
  clusters: ICluster[];
}

export class ClusterList extends React.Component<IClusterListProps, IClusterListState> {
  private _app: JupyterFrontEnd;
  constructor(props: IClusterListProps) {
    super(props);
    this.state = { clusters: props.store.clusters };
    this._app = props.app;
  }

  componentDidMount(): void {
    this.props.store.clusterChaged.connect(this._onClusterUpdate, this);
  }

  componentWillUnmount(): void {
    this.props.store.clusterChaged.disconnect(this._onClusterUpdate, this);
  }

  async forceUpdate(): Promise<void> {
    await this.props.store.forceUpdate();
  }

  _onClusterUpdate(emitter: ClusterStore, newClusters: IChangedArgs<ICluster[] | undefined>): void {
    let newClusterList: ICluster[];
    if (newClusters.newValue) {
      newClusterList = newClusters.newValue;
    } else {
      newClusterList = [];
    }
    this.setState({ clusters: newClusterList });
  }

  render(): JSX.Element {
    const { clusters } = this.state;
    let listing;
    const renderedClusters = clusters
      .filter((cluster) => cluster.status !== ClusterStatus.NEW)
      .sort(compareStatus);

    if (clusters.length > 0) {
      listing = renderedClusters.map((cluster) => {
        return (
          <ClusterListItem
            forceUpdate={() => this.forceUpdate()}
            cluster={cluster}
            app={this._app}
          />
        );
      });
    } else {
      listing = <EmptyClustersList />;
    }
    // Return the JSX component.
    return (
      <div className="bodo-ClusterManager">
        <div className="bodo-ClusterListing">
          <h2>Bodo Clusters</h2>
          <ul className="bodo-ClusterListing-list">{listing}</ul>
        </div>
        {clusters.filter((cluster) => cluster.status === ClusterStatus.INITIALIZING).length !==
        0 ? (
          <div className="bodo-ClusterListing-warning">
            *Connecting to an initializing cluster is not recommended and for debugging purposes
            only
          </div>
        ) : null}
      </div>
    );
  }
}

export class BodoClusterListSidebar extends ReactWidget {
  private _store: ClusterStore;
  private _app: JupyterFrontEnd;

  constructor(store: ClusterStore, app: JupyterFrontEnd) {
    super();
    this.addClass('bodo-Sidebar');
    this._store = store;
    this._app = app;
  }

  render(): JSX.Element {
    return <ClusterList store={this._store} app={this._app} />;
  }
}
