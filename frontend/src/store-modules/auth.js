import axios from '../components/http/Http.js'
import router from '../router.js'
import notify from '../components/notifications/Notify.js'
import store from '../store.js';


const state = {
    accesstoken: null,
    refreshtoken: null
}

const getters = {
    getAuth (state) {
        return state.accesstoken ? true : false
    }
}

const mutations = {
    setAccessToken (state, token) {
        if (token === null) {
            sessionStorage.removeItem('accesstoken')
        } else {
            axios.defaults.headers.common['Authorization'] = `Bearer ${ token }`
            sessionStorage.setItem('accesstoken', token)
        }
        state.accesstoken = token
    },
    setRefreshToken (state, token) {
        if (token === null) {
            sessionStorage.removeItem('refreshtoken')
        } else {
            sessionStorage.setItem('refreshtoken', token)
        }
        state.refreshtoken = token
    }
}

const actions = {
    login: function({commit, dispatch, rootState}, authData) {
        axios.post('/token/', {
            username: authData.username,
            password: authData.password
        })
        .then(res => {
            commit('setAccessToken', res.data.access)
            commit('setRefreshToken', res.data.refresh)
            dispatch('setTimer')
            dispatch('fetchLists')
            .then(() => {
                let user = rootState.user.users.find(function(u) {
                    return u.username === authData.username
                })
                commit('setUser', user)
                notify('Du er logget ind', 'success')
                dispatch('postLogin')
            })
            .catch(err => {
                console.log(err)
            })
        })
        .catch(err => {
            notify('Log ind fejlede', 'error', err)
            dispatch('clearAuth')
        })
    },
    setTimer: function({dispatch}) {
        setTimeout(() => {
            dispatch('refreshToken')
        }, 270000);
    },
    postLogin: function({dispatch}) {
        router.push('/')
    },
    refreshToken: function({commit, dispatch, state}) {
        if (state.refreshtoken) {    
            axios.post('/token/refresh/', {
                refresh: state.refreshtoken
            })
            .then(res => {
                commit('setAccessToken', res.data.access)
                dispatch('setTimer')
            })
            .catch(err => {
                notify('Refresh login fejlede', 'error', err)
                dispatch('clearAuth')
            })
        }
    },
    autoLogin: function({commit, dispatch, rootState}) {
        // check for tokens in session storage and refresh session
        const refreshtoken = sessionStorage.getItem('refreshtoken')
        const accesstoken = sessionStorage.getItem('accesstoken')
        const user_id = parseInt(sessionStorage.getItem('userid'))
        if (refreshtoken) {
            commit('setAccessToken', accesstoken)
            commit('setRefreshToken', refreshtoken)
            dispatch('fetchLists')
            .then(res => {
                let user = rootState.user.users.find(function(u) {
                    return u.id === user_id
                })
                commit('setUser', user)
                dispatch('postLogin')
                dispatch('refreshToken')
            })
            .catch(err => {
                console.log(err)
            })
        } else {
            dispatch('clearAuth')
        }
    },
    logout: function({dispatch}) {
        dispatch('clearAuth')
        notify('Du er logget ud')
    },
    clearAuth: function ({commit}) {
        commit('setAccessToken', null)
        commit('setRefreshToken', null)
        commit('setUser', null)
        router.replace('/login')
    }
}

export default {
    state,
    getters,
    mutations,
    actions
}