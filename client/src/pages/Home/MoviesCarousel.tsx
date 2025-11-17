import { Heading, Box } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import PageAlert from '~/components/PageAlert';
import Carousel from './Carousel';
import { useGetMoviesQuery } from '~/store/api/movieSlice';
import type { IMoviesParams, IMoviesResultTypeEnum } from '~/types/movie';
import { HEADING_MAP } from '~/consts/movies';
import { type IError } from '~/types/error';
import styles from './styles/carousel-styles';

type IProps = {
  resultType: IMoviesResultTypeEnum;
  href: string;
};

const MoviesCarousel = ({ resultType, href }: IProps) => {
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
      <ReactRouterLink to={href}>
        <Heading size="2xl" color="accent.solid" padding="20px" ml="10px" _hover={{ color: 'accent.emphasized' }}>
          {HEADING_MAP[resultType]}
        </Heading>
      </ReactRouterLink>
      <Carousel isFetching={isFetching} movies={data?.movies} />
    </Box>
  );
};

export default MoviesCarousel;
