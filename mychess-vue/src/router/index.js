import { createRouter, createWebHistory } from 'vue-router'
import LogInView from '../views/LogInView.vue'
import SignUpView from '../views/SignUpView.vue'
import LogOutView from '../views/LogOutView.vue'
import CreateGameView from '../views/CreateGameView.vue'
import PlayView from '../views/PlayView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/log-in',
      name: 'home_page',
      component: LogInView
    },
    {
      path: '/',
      redirect: '/log-in'
    },
    {
      path: '/sign-up',
      name: 'sign_up',
      component: SignUpView
    },
    {
      path: '/log-out',
      name: 'log_out',
      component: LogOutView
    },
    {
      path: '/creategame',
      name: 'create_game',
      component: CreateGameView
    },
    {
      path: '/play',
      name: 'play_game',
      component: PlayView
    }
  ]
})

export default router
