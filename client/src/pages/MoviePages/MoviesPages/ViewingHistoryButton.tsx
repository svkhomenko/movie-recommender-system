import { IconButton } from '@chakra-ui/react';
import { useRemoveMovieFromViewingHistoryMutation } from '~/store/api/movieSlice';
import useRequestHandler from '~/hooks/useRequestHandler';
import { Tooltip } from '~/components/ui/tooltip';
import { TiDelete } from 'react-icons/ti';
import { type IMovieFromList } from '~/types/movie';
import { stylesMediumCard } from '../movie-card.styles';

type IProps = {
  movie: IMovieFromList;
};

const ViewingHistoryButton = ({ movie }: IProps) => {
  const [removeFromViewingHistory, { isLoading }] = useRemoveMovieFromViewingHistoryMutation();

  const { handler: removeFromViewingHistoryHandler } = useRequestHandler<number>({
    f: removeFromViewingHistory,
    successMsg: 'Movie was removed from viewing history.',
  });

  return (
    <Tooltip content="Remove from viewing history" contentProps={{ css: { '--tooltip-bg': '#17233b' } }}>
      <IconButton
        aria-label="ViewingHistory"
        variant="ghost"
        size="md"
        css={stylesMediumCard.viewingHistoryButton}
        onClick={(e) => {
          e.preventDefault();
          removeFromViewingHistoryHandler(movie.id);
        }}
        loading={isLoading}
      >
        <TiDelete />
      </IconButton>
    </Tooltip>
  );
};

export default ViewingHistoryButton;
