import { defineStore } from 'pinia'

export const useTokenStore = defineStore("tokens",
{
    state: () => ({
        token: null,
        isAuthenticated: false,
        user_id: null,
        gameData: null,
    }),
    actions: {
        setToken(token, user_id){
            this.token = token
            this.isAuthenticated = true
            this.user_id = user_id
        },
        removeToken() {
            this.token = null
            this.isAuthenticated = false
            this.user_id = null
        },
        setGameData(gameData){
            this.gameData = gameData
        },
        restoreGameData(){
            this.gameData = null
        },
    },
})