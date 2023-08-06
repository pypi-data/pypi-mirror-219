/* This file creates custom dropdowns and additions to the jupyter notebook toolbar
 * including the cluster attach dropdown and the catalog select dropdown (controlled by a feature flag).
 * */

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ISessionContext, ReactWidget, showErrorMessage } from '@jupyterlab/apputils';
import { DocumentRegistry } from '@jupyterlab/docregistry';
import { INotebookModel, NotebookPanel } from '@jupyterlab/notebook';
import { IDisposable, DisposableDelegate } from '@lumino/disposable';
import { IChangedArgs } from '@jupyterlab/coreutils';
import { createRemoteIKernelHandler, fetchConfig } from './handler';
import * as React from 'react';
import { ClusterStore } from './store';
import { ClusterStatus, ICluster } from './types';
import ClusterSelectList from './clusterSelect';
import { CatalogsSelect } from './catalogSelect';

interface IProps {
  store: ClusterStore;
  startKernelForCluster: (clusterUUID?: string) => Promise<boolean>;
  getClusterUUIDFromKernel: (kernelName: string) => Promise<any>;
  sessionContext: ISessionContext;
}

interface IState {
  clusters: ICluster[];
  currentClusterUUID: string | null;
  autoAttachState: boolean | null;
  clusterAttachloading: boolean;
}

class ClusterSelect extends React.Component<IProps, IState> {
  constructor(props: IProps) {
    super(props);
    this.state = {
      clusters: props.store.clusters,
      currentClusterUUID: null,
      autoAttachState: null,
      clusterAttachloading: false,
    };
    this._tryAutoAttach();
  }

  componentDidMount() {
    this.props.store.clusterChaged.connect(this._onClusterUpdate, this);
    this.props.sessionContext.sessionChanged.connect(this._onSessionUpdate, this);
  }

  componentWillUnmount() {
    this.props.store.clusterChaged.disconnect(this._onClusterUpdate, this);
    this.props.sessionContext.sessionChanged.disconnect(this._onSessionUpdate, this);
  }

  async _onSessionUpdate(emitter: ISessionContext, newSession: any): Promise<void> {
    console.log('Detected Session Change.');
    const { clusters } = this.state;
    if (newSession.newValue?._kernel?._name) {
      console.debug('Session Change New Kernel Name: ', newSession.newValue._kernel._name);

      // If the kernel is the dummy kernel, don't do anything
      if (newSession.newValue._kernel._name === 'bodo_platform_dummy_kernel') {
        return;
      }

      this.props.getClusterUUIDFromKernel(newSession.newValue._kernel._name).then(
        (clusterUUID) => {
          const clusterFromKernel = clusters.find((cluster) => cluster.uuid === clusterUUID);
          if (clusterFromKernel && clusterFromKernel.status === ClusterStatus.RUNNING) {
            console.debug('Found cluster for this kernel: ', clusterUUID);
            this.setState({ currentClusterUUID: clusterUUID });
          } else {
            console.debug('Cluster not found or not running, setting currentClusterUUID to null.');
            this.setState({ currentClusterUUID: null });
            this.props.startKernelForCluster(); // No Kernel
          }
        },
        (reason: any) => {
          console.error('Error while getting cluster UUID from kernel: ', reason);
          console.error('Setting currentClusterUUID to null.');
          this.setState({ currentClusterUUID: null });
        }
      );
    } else {
      console.debug('Session has no kernel. Setting currentClusterUUID to null.');
      this.setState({ currentClusterUUID: null });
    }
  }

  async _onClusterUpdate(
    emitter: ClusterStore,
    newClusters: IChangedArgs<ICluster[] | undefined>
  ): Promise<void> {
    const { currentClusterUUID } = this.state;

    let newClusterList: ICluster[];
    if (newClusters.newValue) {
      newClusterList = newClusters.newValue;
    } else {
      newClusterList = [];
    }
    let newCurrentClusterUUID = currentClusterUUID;
    if (currentClusterUUID && !newClusterList.map((x) => x.uuid).includes(currentClusterUUID)) {
      newCurrentClusterUUID = null;
      await showErrorMessage(
        'Cluster not available anymore!',
        'The cluster was removed or is being modified. Your session will be shutdown.'
      );
      await this.props.startKernelForCluster(); // Change to no kernel
    }

    this.setState({
      clusters: newClusterList,
      currentClusterUUID: newCurrentClusterUUID,
    });

    await this._tryAutoAttach();
  }

  async _tryAutoAttach(): Promise<void> {
    const { clusters, currentClusterUUID, autoAttachState } = this.state;
    let autoAttach = autoAttachState;
    let newCurrentClusterUUID = currentClusterUUID;
    // Since non-running clusters are now fetched due to the addition of pausing and
    // unpausing, clusters need to be filtered down to those that are running.
    const runningClusters = clusters.filter((cluster) => cluster.status === ClusterStatus.RUNNING);
    this.setState({ clusterAttachloading: true });
    // If autoAttach hasn't been fetched from the backend yet
    // fetch it. Since the response from the backend won't change
    // only fetch it once.
    if (autoAttachState === null) {
      autoAttach = (await fetchConfig()).auto_attach;
    }
    // If the notebook isn't attached to a cluster, there is only one cluster available
    // and is configured to have autoAttach enabled then start a kernel on the cluster
    // and set it as the currently attached cluster
    if (!currentClusterUUID && runningClusters.length === 1 && autoAttach) {
      this.props.startKernelForCluster(runningClusters[0].uuid).then((success) => {
        if (success) {
          newCurrentClusterUUID = runningClusters[0].uuid;
        }
      });
    }

    this.setState({
      currentClusterUUID: newCurrentClusterUUID,
      autoAttachState: autoAttach,
      clusterAttachloading: false,
    });
  }

  selectClusterCallback(clusterUUID: string) {
    console.debug('[onSelectCluster] clusterUUID: ', clusterUUID);
    this.setState({ clusterAttachloading: true });
    const { startKernelForCluster } = this.props;
    if (clusterUUID === '0') {
      startKernelForCluster(); // Change to "No Kernel"
      this.setState({ currentClusterUUID: null, clusterAttachloading: false });
    } else {
      startKernelForCluster(clusterUUID).then((success) => {
        if (success) {
          this.setState({ currentClusterUUID: clusterUUID, clusterAttachloading: false });
        } else {
          this.setState({ currentClusterUUID: null, clusterAttachloading: false });
        }
      });
    }
  }

  render() {
    const { clusters, currentClusterUUID, clusterAttachloading } = this.state;
    return (
      <ClusterSelectList
        store={this.props.store}
        clusterAttachloading={clusterAttachloading}
        myOnChange={this.selectClusterCallback.bind(this)}
        clusters={clusters}
        currentClusterUUID={currentClusterUUID}
      />
    );
  }
}

export class ToolbarExtension
  implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel>
{
  private _store: ClusterStore;
  // Feature flag that controls whether catalogs are enabled.
  private _catalog_mode: boolean | null;

  constructor(store: ClusterStore, catalog_mode: boolean | null) {
    this._store = store;
    this._catalog_mode = catalog_mode;
    // Catalog mode is picked up from configuration, where it is set using
    // the default notebook config built from
    // the backend. True if AWS or non-pro environments for now.
    this._setCatalogMode();
  }

  async _setCatalogMode(): Promise<void> {
    let catalogmode = this._catalog_mode;
    if (catalogmode === null) {
      catalogmode = (await fetchConfig()).catalog_mode;
    }
    this._catalog_mode = catalogmode;
  }

  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    const endKernel = async () => {
      await context.sessionContext.shutdown();
      return true;
    };

    const startKernelForCluster = async (clusterUUID?: string) => {
      if (!clusterUUID) {
        console.log('No clusterUUID. Shutting session down...');
        return endKernel();
      }

      console.log('Starting Kernel for clusterUUID: ', clusterUUID);

      console.debug(
        'Contacting Jupyter Server App to start remote kernel for clusterUUID: ',
        clusterUUID
      );
      let remoteKernelName: string;
      try {
        remoteKernelName = await createRemoteIKernelHandler(clusterUUID);
      } catch (e) {
        console.error('Unable to register a remote kernel: ', e);
        showErrorMessage(
          'Bodo Extension Error: Unable to create a remote kernel on the cluster.',
          e
        );
        return false;
      }
      console.log('Refreshing kernel specs and changing to remote kernel: ', remoteKernelName);

      // Refresh the list of kernels
      await context.sessionContext.specsManager.refreshSpecs();
      // Switch to the remote kernel for this cluster
      await context.sessionContext.changeKernel({ name: remoteKernelName });
      return true;
    };

    const getClusterUUIDFromKernel = async (kernelName: string) => {
      console.debug('[getClusterUUIDFromKernel] kernelName: ', kernelName);
      console.debug(
        '[getClusterUUIDFromKernel] KernelSpecs: ',
        context.sessionContext.specsManager.specs?.kernelspecs
      );
      if (
        context.sessionContext.specsManager.specs &&
        kernelName in context.sessionContext.specsManager.specs.kernelspecs
      ) {
        const kernelspec = context.sessionContext.specsManager.specs.kernelspecs[kernelName];
        if (kernelspec) {
          const metadata = kernelspec.metadata;
          if (metadata) {
            if ('BodoClusterUUID' in metadata) {
              return metadata['BodoClusterUUID'];
            }
          }
        }
      }
      return null;
    };

    const queryClient = new QueryClient();

    const clusterSelectDropdown = ReactWidget.create(
      <QueryClientProvider client={queryClient}>
        <ClusterSelect
          store={this._store}
          startKernelForCluster={startKernelForCluster}
          getClusterUUIDFromKernel={getClusterUUIDFromKernel}
          sessionContext={context.sessionContext}
        />
      </QueryClientProvider>
    );

    const catalogSelectDropdown = ReactWidget.create(
      <QueryClientProvider client={queryClient}>
        <CatalogsSelect panel={panel} />
      </QueryClientProvider>
    );

    panel.toolbar.insertItem(0, 'clusterSelect', clusterSelectDropdown);
    const enable_catalog = this._catalog_mode;
    if (enable_catalog) {
      panel.toolbar.insertItem(10, 'catalogSelect', catalogSelectDropdown);
    }

    return new DisposableDelegate(() => {
      clusterSelectDropdown.dispose();
      if (enable_catalog) {
        catalogSelectDropdown.dispose();
      }
    });
  }
}
