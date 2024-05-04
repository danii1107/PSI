import { defineStore } from 'pinia'

export const useTokenStore = defineStore("tokens",
{
    state: () => ({
        token: null,
        isAuthenticated: false,
    }),
    actions: {
        setToken(token){
            this.token = token
            this.isAuthenticated = true
        },
        removeToken() {
            this.token = null
            this.isAuthenticated = false
        },
    },
})