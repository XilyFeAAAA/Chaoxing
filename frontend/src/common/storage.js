import * as constants from './constant'

// 存储短token
export const setAccessToken = (token) => localStorage.setItem(constants.ACCESS_TOKEN, token)
// 存储长token
export const setRefreshToken = (token) => localStorage.setItem(constants.REFRESH_TOKEN, token)
// 获取短token
export const getAccessToken = () => localStorage.getItem(constants.ACCESS_TOKEN)
// 获取长token
export const getRefreshToken = () => localStorage.getItem(constants.REFRESH_TOKEN)
// 删除短token
export const removeAccessToken = () => localStorage.removeItem(constants.ACCESS_TOKEN)
// 删除长token
export const removeRefreshToken = () => localStorage.removeItem(constants.REFRESH_TOKEN)
