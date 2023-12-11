import request from './http'

export const login = (params) => request.post('/auth/access-token', params)

export const getme = () => request.get('/user/me')

export const getaccounts = () => request.get('/chaoxing/accounts')

export const register = (data) => request.post('/user/add', data)

export const pwd_bind_account = (data) => request.post('/chaoxing/pwd-bind', data)

export const qrcode_bind_account = (data) => request.post('/chaoxing/qrcode-bind', data)

export const refresh_account = (data) => request.post('/chaoxing/refresh', data)

export const del_account = (data) => request.post('/chaoxing/account/del', data)

export const active_account = (data) => request.post('/chaoxing/account/active', data)

export const get_courses = () => request.get('/chaoxing/courses')

export const sumbit_course_order = (data) => request.post('/chaoxing/order/submit', data, {showLoading: true})

export const get_course_orders = (params) => request.get('/chaoxing/order', { params })

export const get_qrcode = () => request.get('/chaoxing/qrcode', { responseType: 'blob' })

export const get_setting = (type) => request.get(`/user/setting/${type}`)

export const set_setting = (type, setting) => request.post(`/user/setting/${type}`, setting)

export const get_notification = () => request.get('/user/notification')

export const refresh_course = () => request.post('/chaoxing/courses/refresh')

export const get_admin_courseorder = (data) =>
    request.post(`/admin/order/course?limit=${data.limit}&cursor=${data.cursor}`, data.keyword, {
        showLoading: true,
    })

export const get_admin_memberlist = (data) =>
    request.post(`/admin/user/member?limit=${data.limit}&cursor=${data.cursor}`, data.keyword, {
        showLoading: true
    })

export const del_notificaion = () => request.post('/user/notification/delete')

export const read_notification = (ids) => request.post('/user/notification/read', {ids})

export const pre_confirm = (data) => request.post('/chaoxing/order/pre', data)

export const get_confrim = (order_id) => request.get(`/chaoxing/order/${order_id}`)

export const cancel_order = (order_id) => request.post(`/chaoxing/order/cancel/${order_id}`)

export const get_admin_permission = (data) =>
    request.post(`/admin/permissions?limit=${data.limit}&cursor=${data.cursor}`, data.keyword, {
        showLoading: true
    })

export const get_admin_role = (data) =>
    request.post(`/admin/roles?limit=${data.limit}&cursor=${data.cursor}`, data.keyword, {
        showLoading: true
    })

export const get_admin_logger = (data) =>
    request.post(`/admin/logs?limit=${data.limit}&cursor=${data.cursor}`, data.keyword, {
        showLoading: true
    })


export const admin_login = (data) => request.post('/admin/login', data)
