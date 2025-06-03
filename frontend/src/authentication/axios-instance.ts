import axiosInstance from "axios";
import {serverIP} from './global-vars';

axiosInstance.defaults.baseURL = 'http://' + serverIP + '/';

export default axiosInstance;