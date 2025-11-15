import { Flex, IconButton } from '@chakra-ui/react';
import {
  useAddMovieToWatchLaterMutation,
  useRemoveMovieFromWatchLaterMutation,
  useAddMovieToWatchedMutation,
  useRemoveMovieFromWatchedMutation,
} from '~/store/api/movieSlice';
import useRequestHandler from '~/hooks/useRequestHandler';
import { Tooltip } from '~/components/ui/tooltip';
import { BsBookmark, BsBookmarkFill } from 'react-icons/bs';
import { FiEye, FiEyeOff } from 'react-icons/fi';
import { type IMovie } from '~/types/movie';
import styles from '../movie-card.styles';

type IProps = {
  movie: IMovie;
};

const WatchLaterButton = ({ movie }: IProps) => {
  const [addToWatchLater, { isLoading: isLoadingAdd }] = useAddMovieToWatchLaterMutation();

  const { handler: addToWatchLaterHandler } = useRequestHandler<number>({
    f: addToWatchLater,
    successMsg: 'Movie was added to watch later.',
  });

  const [removeFromWatchLater, { isLoading: isLoadingRemove }] = useRemoveMovieFromWatchLaterMutation();

  const { handler: removeFromWatchLaterHandler } = useRequestHandler<number>({
    f: removeFromWatchLater,
    successMsg: 'Movie was removed from watch later.',
  });

  if (!movie.watch_later) {
    return (
      <Tooltip content="Add to watch later">
        <IconButton
          aria-label="Watch later"
          size="md"
          variant="ghost"
          onClick={() => addToWatchLaterHandler(movie.id)}
          loading={isLoadingAdd}
        >
          <BsBookmark />
        </IconButton>
      </Tooltip>
    );
  }

  return (
    <Tooltip content="Remove from watch later">
      <IconButton
        aria-label="Watch later"
        size="md"
        variant="ghost"
        onClick={() => removeFromWatchLaterHandler(movie.id)}
        loading={isLoadingRemove}
      >
        <BsBookmarkFill />
      </IconButton>
    </Tooltip>
  );
};

const WatchedButton = ({ movie }: IProps) => {
  const [addToWatched, { isLoading: isLoadingAdd }] = useAddMovieToWatchedMutation();

  const { handler: addToWatchedHandler } = useRequestHandler<number>({
    f: addToWatched,
    successMsg: 'Movie was marked as watched.',
  });

  const [removeFromWatched, { isLoading: isLoadingRemove }] = useRemoveMovieFromWatchedMutation();

  const { handler: removeFromWatchedHandler } = useRequestHandler<number>({
    f: removeFromWatched,
    successMsg: 'Movie was marked as unwatched.',
  });

  if (!movie.watched) {
    return (
      <Tooltip content="Mark as watched">
        <IconButton
          aria-label="Watched"
          size="md"
          variant="ghost"
          onClick={() => addToWatchedHandler(movie.id)}
          loading={isLoadingAdd}
        >
          <FiEyeOff />
        </IconButton>
      </Tooltip>
    );
  }

  return (
    <Tooltip content="Mark as unwatched">
      <IconButton
        aria-label="Watched"
        size="md"
        variant="ghost"
        onClick={() => removeFromWatchedHandler(movie.id)}
        loading={isLoadingRemove}
      >
        <FiEye />
      </IconButton>
    </Tooltip>
  );
};

const WatchButtons = ({ movie }: IProps) => {
  return (
    <Flex css={styles.icons}>
      <WatchLaterButton movie={movie} />
      <WatchedButton movie={movie} />
    </Flex>
  );
};

export default WatchButtons;
