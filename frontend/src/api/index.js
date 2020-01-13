import axios from 'axios';

axios.interceptors.request.use(
    function (config) {
        config.headers['Authorization'] = localStorage.getItem('jwt')
        return config;
    }, function (error) {
        return Promise.reject(error);
    });

export default {
    urls: {
        news: '/news',
        chat: '/chat',
        store: '/store',
        users: '/users',
        login: '/auth/login',
        logout: '/auth/logout',
        uploads: '/uploads'
    },
    axios: axios,
}