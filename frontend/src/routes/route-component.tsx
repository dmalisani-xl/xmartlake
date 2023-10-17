import { Home } from 'pages/home';
import { About } from 'pages/about';
import { NotFound } from 'pages/not-found';
import { RouteName } from './routes';
import { Replay } from 'pages/replay';

const RouteComponent = {
  [RouteName.Home]: Home,
  [RouteName.About]: About,
  [RouteName.NotFound]: NotFound,
  [RouteName.Replay]: Replay,
};

export { RouteComponent };
