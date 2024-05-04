import { defineStore } from 'pinia';

export const useGameStore = defineStore("games",
  {
  //id: 'gameData',
  state: () => ({
    gameData: null
  }),
  actions: {
    setGameData(data) {
      this.gameData = data;
    }
  }
});
