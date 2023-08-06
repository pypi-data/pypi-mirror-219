/* eslint-disable no-async-promise-executor */
import { AxiosError, AxiosInstance } from 'axios';
import { showStandaloneSpinner, showConfirmationStatus, showSuccessPublishDialog, showFailurePublishDialog } from './dialog';
import { Dialog } from '@jupyterlab/apputils';
import { ATLAS_BASE_URL, AWB_BASE_URL } from './config';
import axios from 'axios';
import jwt_decode from 'jwt-decode';

export const axiosHandler = (lab_token: string): AxiosInstance => {
  const atlasClient = axios.create({
      baseURL: ATLAS_BASE_URL,
      headers: {
        Authorization: `Bearer ${lab_token}`,
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        "Accept": 'application/json'
      }
    });
  return atlasClient;
}

export const awbAxiosHandler = (lab_token: string): AxiosInstance => {
  const awbClient = axios.create({
      baseURL: AWB_BASE_URL,
      headers: {
        Authorization: `Bearer ${lab_token}`,
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        "Accept": 'application/json'
      }
    });
  return awbClient;
}

/**
 * GET the lab model / JSON that represents a .ipynb file/notebook from AWB
 *
 * @param awbAxiosHandler Axios client that contains a JWT Bearer token
 * @param lab_token JWT Bearer token
 * @returns Promise<void>
 */
export const getIndependentLabModel = async (awbAxiosHandler: AxiosInstance, lab_token: string) => {
  try {
    const token_info = jwt_decode(lab_token) as { [key: string]: any };
    const version_id = token_info.version_id
    const lab_id = token_info.lab_id

    const labFilename = `${token_info.lab_name}.ipynb`
    const instructions = await awbAxiosHandler.get(`api/v1/labs/${lab_id}/lab_versions/${version_id}/download`).then(result => { return result.data })

    Dialog.flush();
    return {labFilename, body: instructions};

    // handle the decoded token here
  } catch (error) {
    console.log(error)
    throw "Failed to fetch notebook"
  }
};

/**
 * POST the lab model / JSON from the .ipynb file/notebook to AWB
 *
 * @param awbAxiosHandler Axios client that contains a JWT Bearer token
 * @returns Promise<void>
 */
export const postIndependentLabModel = async (
  awbAxiosHandler: AxiosInstance,
  labModel: string,
  lab_token: string
): Promise<void> => {
  let confirmation_status = await showConfirmationStatus('Publishing your lab onto Skills Network...').then((resolve: any) => true).catch((err: any) => false);
  if (!confirmation_status) return;
  showStandaloneSpinner("Publishing your changes...");

  const token_info = jwt_decode(lab_token) as { [key: string]: any };
  const version_id = token_info.version_id
  const lab_id = token_info.lab_id

  return new Promise<void>(async (resolve, reject) => {
    await awbAxiosHandler
      .patch(`api/v1/labs/${lab_id}/lab_versions/${version_id}/update_source_file`, {
        file: labModel
      })
      .then(res => {
        console.log('SUCCESSFULLY PUSHED', res);
        Dialog.flush(); //remove spinner
        showSuccessPublishDialog();
        resolve;
      })
      .catch((error: AxiosError) => {
        console.log(error);
        Dialog.flush(); // remove spinner
        showFailurePublishDialog();
        reject;
      });
  });
};

/**
 * GET the lab model / JSON that represents a .ipynb file/notebook from ATLAS
 *
 * @param axiosHandler Axios client that contains a JWT Bearer token
 * @returns Promise<void>
 */
export const getLabModel = (axiosHandler: AxiosInstance) => {
  // GET the lab model
  return axiosHandler
    .get('v1/labs')
    .then(result => {
      Dialog.flush(); //remove spinner
      return result.data;
    })
    .catch(error => {
      console.log(error);
      throw "Failed to fetch notebook"
    });
};

/**
 * POST the lab model / JSON from the .ipynb file/notebook to ATLAS
 *
 * @param axiosHandler Axios client that contains a JWT Bearer token
 * @returns Promise<void>
 */
export const postLabModel = async (
  axiosHandler: AxiosInstance,
  labModel: string
): Promise<void> => {
  let confirmation_status = await showConfirmationStatus('Publishing your lab onto Skills Network...').then((resolve: any) => true).catch((err: any) => false);
  if (!confirmation_status) return;
  showStandaloneSpinner("Publishing your changes...");

  return new Promise<void>(async (resolve, reject) => {
    await axiosHandler
      .post('v1/labs', {
        body: labModel
      })
      .then(res => {
        console.log('SUCCESSFULLY PUSHED', res);
        Dialog.flush(); //remove spinner
        showSuccessPublishDialog();
        resolve;
      })
      .catch((error: AxiosError) => {
        console.log(error);
        Dialog.flush(); // remove spinner
        showFailurePublishDialog();
        reject;
      });
  });
};
