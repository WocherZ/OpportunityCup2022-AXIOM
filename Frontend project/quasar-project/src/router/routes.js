
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/TransactionsPage.vue'), },
      { path: '/transactions', component: () => import('pages/TransactionsPage.vue'), },
      { path: '/charts', component: () => import('pages/ChartsPage.vue'), },
      { path: '/patterns_guide', component: () => import('pages/PatternsGuidePage.vue'), },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
