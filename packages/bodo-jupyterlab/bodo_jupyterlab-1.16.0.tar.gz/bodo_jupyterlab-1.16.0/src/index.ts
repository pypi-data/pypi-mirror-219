import { ILabShell, JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ClusterStore } from './store';
import { ToolbarExtension } from './toolbar';
import { cellFactory } from './cellSelect';
import { LabIcon } from '@jupyterlab/ui-components';
import clusterSvgStr from '../style/clusters.svg';
import logoBgSvgStr from '../style/bodo-icon-white-bg.svg';
import { BodoClusterListSidebar } from './sidebar';
import { plugin as terminalExtension } from './clusterTerminal/clusterTerminalExtension';
import { splash } from './splashExtension';

const activate = (app: JupyterFrontEnd, labShell: ILabShell): void => {
  console.log('Bodo JupyterLab extension activated!');

  const clusterIcon = new LabIcon({
    name: 'cluster_icon',
    svgstr: clusterSvgStr,
  });
  const bodoIconGreenBg = new LabIcon({
    name: 'bodo_jupyterlab:logo-bg',
    svgstr: logoBgSvgStr,
  });

  const widgets = app.shell.widgets('top');
  let widget = widgets.next();
  while (widget !== undefined) {
    if (widget.id === 'jp-MainLogo') {
      bodoIconGreenBg.element({
        container: widget.node,
        justify: 'center',
        margin: '2px 5px 2px 5px',
        height: 'auto',
        width: '20px',
      });
      break;
    }
    widget = widgets.next();
    console.log('widget', widget);
  }

  const _cluster_store = new ClusterStore();

  // Toolbar (select cluster from inside notebook)
  app.docRegistry.addWidgetExtension('Notebook', new ToolbarExtension(_cluster_store, null));
  // Sidebar to display clusters
  const sidebar = new BodoClusterListSidebar(_cluster_store, app);
  sidebar.id = 'bodo-cluster-list';
  sidebar.title.icon = clusterIcon;
  sidebar.title.caption = 'Bodo Clusters';

  labShell.add(sidebar, 'left', { rank: 200 });
};

/**
 * Initialization for the bodo-jupyterlab extension.
 */
const plugins: JupyterFrontEndPlugin<any>[] = [
  {
    id: 'bodo-labextension:plugin',
    autoStart: true,
    requires: [ILabShell],
    activate,
  },
  terminalExtension,
  splash,
  cellFactory,
];

export default plugins;
