import request from './http'

export const login = (params) => request.post('/auth/access-token', params)

export const getme = () => request.get('/user/me')