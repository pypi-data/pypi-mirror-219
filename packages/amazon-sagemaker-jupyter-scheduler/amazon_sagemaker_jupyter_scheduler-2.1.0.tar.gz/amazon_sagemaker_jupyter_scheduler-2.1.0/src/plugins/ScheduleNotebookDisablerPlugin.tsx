/* eslint-disable no-console */
import { JupyterFrontEnd, JupyterFrontEndPlugin, ILabShell } from '@jupyterlab/application';
import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';

import { pluginIds, featureNames } from '../constants/common';

const ScheduleNotebookDisablerPlugin: JupyterFrontEndPlugin<void> = {
  id: pluginIds.SchedulerDisablerPlugin,
  requires: [ILabShell as any],
  autoStart: true,
  activate: (app: JupyterFrontEnd, labShell: ILabShell) => {
    (async () => {
      await app.started;
      await labShell.restored;

      const settings = ServerConnection.makeSettings();
      const requestUrl = URLExt.join(settings.baseUrl, '/sagemaker_feature_enabled');

      const STATIC_FEATURE_LAUNCH_TIME = 1669824000000;

      let currentTime = Date.now();

      const featureApiResponse = await ServerConnection.makeRequest(
        requestUrl,
        { method: 'POST', body: JSON.stringify({ feature_name: featureNames.scheduler }) },
        settings,
      );

      let featureDisabledFromWebAppSettings = false;

      try {
        const featureApiResponseBody = await featureApiResponse.json();
        if (featureApiResponseBody.currentTime) {
          currentTime = parseInt(featureApiResponseBody.currentTime);
        }
        if (featureApiResponse.status === 200) {
          if (featureApiResponseBody.feature_found === true && featureApiResponseBody.feature_enabled === false) {
            featureDisabledFromWebAppSettings = true;
          }
        }
      } catch (err) {
        // TODO: log error if API call fails
      }

      const getEnabledFeaturesFromCookie = (): string | null => {
        const documentCookie = document.cookie || '';
        // Split cookie string and get all individual name=value pairs in an array
        const cookieArr = documentCookie.split(';');

        for (let i = 0; i < cookieArr.length; i++) {
          const cookiePair = cookieArr[i].split('=');

          /**
           * Removing whitespace at the beginning of the cookie name
           * and compare it with the given string
           */
          if (cookiePair[0].trim() === 'enabledFeatureFlags') {
            // Decode the cookie value and return
            return JSON.parse(decodeURIComponent(cookiePair[1]));
          }
        }

        // Return null if not found
        return null;
      };

      const enabledFeaturesFromCookie = getEnabledFeaturesFromCookie();
      const nbSchedulerEnabledFromCookie = enabledFeaturesFromCookie
        ? enabledFeaturesFromCookie.indexOf(featureNames.scheduler) >= 0
        : false;

      const featureDisabledFromStaticLaunchTime = currentTime < STATIC_FEATURE_LAUNCH_TIME;
      const shouldDisableScheduler =
        (featureDisabledFromStaticLaunchTime || featureDisabledFromWebAppSettings) && !nbSchedulerEnabledFromCookie;

      if (shouldDisableScheduler) {
        document.styleSheets[0].insertRule(
          'li[data-command="scheduling:create-from-filebrowser"] { display: none !important; }',
        );

        document.styleSheets[0].insertRule(`
          button[title="Create a notebook job"] { display: none !important; }
        `);

        document.styleSheets[0].insertRule(`
          div[class="jp-LauncherCard"][title="Notebook Jobs"] { display: none !important; }
        `);
      }
    })();
  },
};

export { ScheduleNotebookDisablerPlugin };
