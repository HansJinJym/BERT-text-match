export default class ApiUtil {
    static URL_IP = 'http://127.0.0.1:5001';
    static URL_ROOT = '/api/v1';
 
    static API_SEARCH = ApiUtil.URL_ROOT + '/search';  // 发送查询query
    static API_LIST = ApiUtil.URL_ROOT + '/list';      // 取回查询结果
    static API_FEEDBACk = ApiUtil.URL_ROOT + '/feedback';
}

