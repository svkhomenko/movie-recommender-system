import { useState } from 'react';
import { Heading, Center } from '@chakra-ui/react';
import MovieSearch from './MovieSearch';
import MovieFilters from './MovieFilters';
import MoviesList from './MoviesList';
import { MOVIES_RESULT_TYPES, HEADING_MAP } from '~/consts/movies';
import type { IMoviesResultTypeEnum } from '~/types/movie';

type IProps = {
  headingType?: IMoviesResultTypeEnum;
};

const MoviesPage = ({ headingType = MOVIES_RESULT_TYPES.BEST_RATING }: IProps) => {
  const [q, setQ] = useState<string>('');
  const [yearMin, setYearMin] = useState<number | null>(null);
  const [yearMax, setYearMax] = useState<number | null>(null);
  const [genreIds, setGenreIds] = useState<number[]>([]);

  return (
    <>
      <Center>
        <Heading size="2xl" color="accent.solid" padding="20px">
          {HEADING_MAP[headingType]}
        </Heading>
      </Center>
      <MovieSearch setQ={setQ} />
      <MovieFilters setYearMin={setYearMin} setYearMax={setYearMax} setGenreIds={setGenreIds} />
      <MoviesList q={q} yearMin={yearMin} yearMax={yearMax} genreIds={genreIds} resultType={headingType} />
    </>
  );
};

export default MoviesPage;
