// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// based on https://github.com/jupyterlab/jupyterlab/blob/5b334692b251af0156ed1a4e9298f2bc1f279c9e/packages/apputils-extension/src/index.ts#L169

import { JupyterFrontEndPlugin, JupyterFrontEnd } from '@jupyterlab/application';
import { ISplashScreen } from '@jupyterlab/apputils';
import { ITranslator } from '@jupyterlab/translation';
import { Dialog } from '@jupyterlab/apputils';
import { Throttler } from '@lumino/polling';
import { DisposableDelegate } from '@lumino/disposable';
import { LabIcon } from '@jupyterlab/ui-components';
import logoBgSvgStr from '../style/bodo-icon-green.svg';

const SPLASH_RECOVER_TIMEOUT = 12000;

/**
 * The command IDs used by the apputils plugin.
 */
namespace CommandIDs {
  export const loadState = 'apputils:load-statedb';

  export const print = 'apputils:print';

  export const reset = 'apputils:reset';

  export const resetOnLoad = 'apputils:reset-on-load';

  export const runFirstEnabled = 'apputils:run-first-enabled';

  export const runAllEnabled = 'apputils:run-all-enabled';

  export const toggleHeader = 'apputils:toggle-header';

  export const displayShortcuts = 'apputils:display-shortcuts';
}

export const splash: JupyterFrontEndPlugin<ISplashScreen> = {
  id: '@jupyterlab/apputils-extension:bodosplash',
  autoStart: true,
  requires: [ITranslator],
  provides: ISplashScreen,
  activate: (app: JupyterFrontEnd, translator: ITranslator) => {
    const trans = translator.load('jupyterlab');
    const { commands, restored } = app;

    // Create splash element and populate it.
    const splash = document.createElement('div');
    const galaxy = document.createElement('div');
    const logo = document.createElement('div');

    splash.id = 'jupyterlab-splash';
    galaxy.id = 'galaxy';
    logo.id = 'main-logo';
    const bodoIconGreenBg = new LabIcon({
      name: 'bodo_jupyterlab:logo-bg',
      svgstr: logoBgSvgStr,
    });

    bodoIconGreenBg.element({
      container: logo,
      stylesheet: 'splash',
    });

    galaxy.appendChild(logo);
    ['1', '2', '3'].forEach((id) => {
      const moon = document.createElement('div');
      const planet = document.createElement('div');

      moon.id = `moon${id}`;
      moon.className = 'moon orbit';
      planet.id = `planet${id}`;
      planet.className = 'planet';

      moon.appendChild(planet);
      galaxy.appendChild(moon);
    });

    splash.appendChild(galaxy);

    // Create debounced recovery dialog function.
    let dialog: Dialog<unknown> | null;
    const recovery = new Throttler(
      async () => {
        if (dialog) {
          return;
        }

        dialog = new Dialog({
          title: trans.__('Loading…'),
          body: trans.__(`The loading screen is taking a long time.
Would you like to clear the workspace or keep waiting?`),
          buttons: [
            Dialog.cancelButton({ label: trans.__('Keep Waiting') }),
            Dialog.warnButton({ label: trans.__('Clear Workspace') }),
          ],
        });

        try {
          const result = await dialog.launch();
          dialog.dispose();
          dialog = null;
          if (result.button.accept && commands.hasCommand(CommandIDs.reset)) {
            return commands.execute(CommandIDs.reset);
          }

          // Re-invoke the recovery timer in the next frame.
          requestAnimationFrame(() => {
            // Because recovery can be stopped, handle invocation rejection.
            void recovery.invoke().catch((_) => undefined);
          });
        } catch (error) {
          /* no-op */
        }
      },
      { limit: SPLASH_RECOVER_TIMEOUT, edge: 'trailing' }
    );

    // Return ISplashScreen.
    let splashCount = 0;
    return {
      show: (light = true) => {
        splash.classList.remove('splash-fade');
        splash.classList.toggle('light', light);
        splash.classList.toggle('dark', !light);
        splashCount++;
        document.body.appendChild(splash);

        // Because recovery can be stopped, handle invocation rejection.
        void recovery.invoke().catch((_) => undefined);

        return new DisposableDelegate(async () => {
          await restored;
          if (--splashCount === 0) {
            void recovery.stop();

            if (dialog) {
              dialog.dispose();
              dialog = null;
            }

            splash.classList.add('splash-fade');
            window.setTimeout(() => {
              document.body.removeChild(splash);
            }, 200);
          }
        });
      },
    };
  },
};

// export default plugin;
const plugins: JupyterFrontEndPlugin<any>[] = [splash];

export default plugins;
