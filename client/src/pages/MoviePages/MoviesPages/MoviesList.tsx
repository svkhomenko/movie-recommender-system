import { useState, useEffect, type ReactNode } from 'react';
import { Flex, Heading, Grid, ButtonGroup, IconButton, Pagination } from '@chakra-ui/react';
import { LuChevronLeft, LuChevronRight } from 'react-icons/lu';
import Container from '~/components/Container';
import PageAlert from '~/components/PageAlert';
import MovieCardSkeleton from '~/components/MovieCardSkeleton/MovieCardSkeleton';
import MovieCard from './MovieCard';
import { useGetMoviesQuery } from '~/store/api/movieSlice';
import type { IMoviesParams, IMoviesResultTypeEnum } from '~/types/movie';
import { MOVIES_RESULT_TYPES } from '~/consts/movies';
import { type IError } from '~/types/error';

type IProps = {
  q: string;
  yearMin: number | null;
  yearMax: number | null;
  genreIds: number[];
  resultType?: IMoviesResultTypeEnum;
};

const MoviesList = ({ q, yearMin, yearMax, genreIds, resultType = MOVIES_RESULT_TYPES.BEST_RATING }: IProps) => {
  const [curPage, setCurPage] = useState(1);
  const itemsPerPage = 20;

  const params: IMoviesParams = {
    limit: itemsPerPage,
    offset: (curPage - 1) * itemsPerPage,
    result_type: resultType,
  };
  q ? (params.q = q) : (params.q = undefined);
  yearMin ? (params.year_min = yearMin) : (params.year_min = undefined);
  yearMax ? (params.year_max = yearMax) : (params.year_max = undefined);
  genreIds && genreIds.length !== 0 ? (params.genre_ids = genreIds) : (params.genre_ids = undefined);

  useEffect(() => {
    setCurPage(1);
  }, [q, yearMin, yearMax, genreIds, resultType]);

  const { data, isFetching, error } = useGetMoviesQuery(params);

  if (error) {
    return <PageAlert status="error" message={(error as IError).data.detail} />;
  }

  let content: ReactNode;
  if (isFetching) {
    content = Array.from({ length: itemsPerPage }).map((_, i) => <MovieCardSkeleton key={i} />);
  } else if (data?.movies.length) {
    content = data?.movies.map((movie) => <MovieCard key={movie.id} movie={movie} />);
  }

  return (
    <Container>
      {!isFetching && data?.movies.length == 0 ? (
        <Flex w="100%" alignItems="center" justifyContent="center" mt="40px">
          <Heading size="lg">No movies found</Heading>
        </Flex>
      ) : (
        <Grid templateColumns="repeat(auto-fit, minmax(220px, 1fr))" gap={6} p={{ base: '10px 20px', md: '20px 30px' }}>
          {content}
        </Grid>
      )}

      <Flex w="100%" alignItems="center" justifyContent="center" py="40px">
        {!isFetching && data?.movies.length !== 0 && (
          <Pagination.Root
            count={data?.totalCount as number}
            pageSize={itemsPerPage}
            page={curPage}
            onPageChange={(e) => setCurPage(e.page)}
          >
            <ButtonGroup variant="outline" size="sm">
              <Pagination.PrevTrigger asChild>
                <IconButton>
                  <LuChevronLeft />
                </IconButton>
              </Pagination.PrevTrigger>
              <Pagination.Items
                render={(page) => (
                  <IconButton variant={{ base: 'outline', _selected: 'solid' }}>{page.value}</IconButton>
                )}
              />
              <Pagination.NextTrigger asChild>
                <IconButton>
                  <LuChevronRight />
                </IconButton>
              </Pagination.NextTrigger>
            </ButtonGroup>
          </Pagination.Root>
        )}
      </Flex>
    </Container>
  );
};

export default MoviesList;
