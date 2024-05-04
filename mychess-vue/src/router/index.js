import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'
import LogOutView from '../views/LogOutView.vue'
import CreateGameView from '../views/CreateGameView.vue'
import PlayView from '../views/PlayView.vue'
import { useTokenStore } from '../stores/token'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/log-in',
      name: 'home_page',
      component: LoginView
    },
    {
      path: '/',
      redirect: '/log-in'
    },
    {
      path: '/sign-up',
      name: 'sign_up',
      component: SignupView
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

router.beforeEach(async (to, from, next) => {
  const tokenStore = useTokenStore();

  if (tokenStore.isAuthenticated) {
    next();
    return;
  }

  if (to.name === 'home_page' || to.name === 'sign_up') {
    next();
    return;
  }

  const waitForAuth = new Promise((resolve) => {
    const checkAuth = () => {
      if (tokenStore.isAuthenticated) {
        resolve(true);
      } else {
          setTimeout(checkAuth, 100);
      }
    };
    checkAuth();
  });

  const isAuth = await waitForAuth.catch(() => false);

  if (isAuth) {
    next();
  } else {
    next({ name: 'home_page' });
  }
});

export default router
