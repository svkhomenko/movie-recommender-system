import { Heading, Box } from '@chakra-ui/react';
import PageAlert from '~/components/PageAlert';
import Carousel from './Carousel';
import { useGetMoviesQuery } from '~/store/api/movieSlice';
import type { IMoviesParams, IMoviesResultTypeEnum } from '~/types/movie';
import { MOVIES_RESULT_TYPES, HEADING_MAP } from '~/consts/movies';
import { type IError } from '~/types/error';
import styles from './styles/carousel-styles';

type IProps = {
  resultType?: IMoviesResultTypeEnum;
};

const MoviesCarousel = ({ resultType = MOVIES_RESULT_TYPES.BEST_RATING }: IProps) => {
  const itemsPerPage = 20;
  const params: IMoviesParams = {
    limit: itemsPerPage,
    offset: 0,
    result_type: resultType,
  };

  const { data, isFetching, error } = useGetMoviesQuery(params);

  if (error) {
    return <PageAlert status="error" message={(error as IError).data.detail} />;
  }

  return (
    <Box css={styles.box}>
      <Heading size="2xl" color="accent.solid" padding="20px">
        {HEADING_MAP[resultType]}
      </Heading>
      <Carousel isFetching={isFetching} movies={data?.movies} />
    </Box>
  );
};

export default MoviesCarousel;
