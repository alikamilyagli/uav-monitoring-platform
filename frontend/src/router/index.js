import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Drones from '../views/Drones.vue';
import Tasks from '../views/Tasks.vue';
import TaskImages from '../views/TaskImages.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'Droneqube - UAV Monitoring Platform',
    },
  },
  {
    path: '/drones',
    name: 'Drones',
    component: Drones,
    meta: {
      title: 'Droneqube - Drones',
    },
  },
  {
    path: '/tasks',
    name: 'Tasks',
    component: Tasks,
    meta: {
      title: 'Droneqube - Tasks',
    },
  },
  {
      path: '/tasks/:taskId/images',
      name: 'TaskImages',
      component: TaskImages,
      props: true,
      meta: {
        title: 'Droneqube - Task Images',
      },
    },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior() {
    document.getElementById('app').scrollIntoView();
  },
});

export default router;
