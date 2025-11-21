import { Card, Stack, Heading, Text, Flex, Image, Icon, GridItem, Badge } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import { useGetMoviePosterPathQuery } from '~/store/tmdbApi/tmdbMoviePosterSlice';
import MovieCardSkeleton from '~/components/MovieCardSkeleton/MovieCardSkeleton';
import { FiStar } from 'react-icons/fi';
import { getRealiseDate, getGenres } from '../helpers';
import { IMAGE_BASE_URL, FALLBACK_IMAGE_URL } from '~/consts/images';
import type { IMovieFromList } from '~/types/movie';
import { stylesMediumCard } from '../movie-card.styles';

type IProps = {
  movie: IMovieFromList;
};

const MovieCard = ({ movie }: IProps) => {
  const { data: moviePoster, isLoading: isLoadingPoster } = useGetMoviePosterPathQuery(Number(movie.id));

  if (isLoadingPoster) {
    return <MovieCardSkeleton />;
  }

  return (
    <ReactRouterLink to={`/movies/${movie.id}`}>
      <GridItem>
        <Card.Root css={stylesMediumCard.card}>
          {movie.explanation && <Badge css={stylesMediumCard.explanationBadge}>{movie.explanation}</Badge>}

          <Image
            src={IMAGE_BASE_URL + moviePoster?.poster_path}
            alt={movie.title}
            css={stylesMediumCard.image}
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.onerror = null;
              target.src = FALLBACK_IMAGE_URL;
            }}
          />

          <Card.Body p="10px">
            <Stack gap="1" align="center" textAlign="center">
              <Heading css={stylesMediumCard.heading}>{movie.title}</Heading>

              <Flex alignItems="center" justifyContent="space-between" w="200px">
                <Flex alignItems="center" gap="1" justifyContent="space-between">
                  <Icon as={FiStar} color="accent.solid" boxSize="3" />
                  <Text fontSize="xs" fontWeight="bold">
                    {movie.vote_average}
                  </Text>
                  <Text fontSize="xs" color="neutral.muted">
                    ({movie.vote_count})
                  </Text>
                </Flex>

                <Text css={stylesMediumCard.text}>
                  <span>{getRealiseDate(movie.release_date)}</span>
                </Text>
              </Flex>
              <Text css={stylesMediumCard.text}>{getGenres(movie.genres)}</Text>
            </Stack>
          </Card.Body>
        </Card.Root>
      </GridItem>
    </ReactRouterLink>
  );
};

export default MovieCard;
