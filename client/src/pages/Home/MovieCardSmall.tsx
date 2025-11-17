import { Card, Stack, Heading, Text, Flex, Image, Icon, Spinner, Box } from '@chakra-ui/react';
import { Link as ReactRouterLink } from 'react-router-dom';
import { useGetMoviePosterPathQuery } from '~/store/tmdbApi/tmdbMoviePosterSlice';
import { FiStar } from 'react-icons/fi';
import { getRealiseDate, getGenres } from '~/pages/MoviePages/helpers';
import { IMAGE_BASE_URL, FALLBACK_IMAGE_URL } from '~/consts/images';
import type { IMovieFromList } from '~/types/movie';
import styles from './styles/movie-card-small.styles';

type IProps = {
  movie: IMovieFromList;
};

const MovieCardSmall = ({ movie }: IProps) => {
  const { data: moviePoster, isLoading: isLoadingPoster } = useGetMoviePosterPathQuery(Number(movie.id));

  if (isLoadingPoster) {
    return (
      <Card.Root css={styles.card}>
        <Flex w="100%" h="100%" align="center" justify="center">
          <Spinner size="md" />
        </Flex>
      </Card.Root>
    );
  }

  return (
    <ReactRouterLink to={`/movies/${movie.id}`}>
      <Card.Root css={styles.card}>
        <Image
          src={IMAGE_BASE_URL + moviePoster?.poster_path}
          alt={movie.title}
          css={styles.image}
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.onerror = null;
            target.src = FALLBACK_IMAGE_URL;
          }}
        />

        <Box className="info-overlay" css={styles.infoOverlay}>
          <Stack gap="1" align="flex-start" textAlign="left">
            <Heading css={styles.heading}>{movie.title}</Heading>

            <Flex alignItems="center" gap="1">
              <Icon as={FiStar} color="accent.solid" boxSize="3" />
              <Text fontSize="xs" fontWeight="bold">
                {movie.vote_average}
              </Text>
              <Text fontSize="xs" color="neutral.muted">
                ({movie.vote_count} votes)
              </Text>
            </Flex>

            <Text css={styles.text}>
              <span>{getRealiseDate(movie.release_date)}</span>
            </Text>
            <Text css={styles.text}>{getGenres(movie.genres)}</Text>
          </Stack>
        </Box>
      </Card.Root>
    </ReactRouterLink>
  );
};

export default MovieCardSmall;
