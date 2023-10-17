import { withLayout, LayoutType } from 'hocs/with-layout';
import { Replay } from './replay';

const WrappedReplay = withLayout(LayoutType.Default, Replay);

export { WrappedReplay as Replay };
