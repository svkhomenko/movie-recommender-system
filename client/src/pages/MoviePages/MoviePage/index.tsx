import { Card, Stack, Heading, Text, Flex, Image, IconButton, Icon } from '@chakra-ui/react';
import { useParams } from 'react-router-dom';
import { useAppSelector } from '~/hooks/useAppSelector';
import { useGetMovieQuery } from '~/store/api/movieSlice';
import { useGetMoviePosterPathQuery } from '~/store/tmdbApi/tmdbMoviePosterSlice';
import Layout from '~/components/Layout';
import PageAlert from '~/components/PageAlert';
import Loader from '~/components/Loader';
import { Tooltip } from '~/components/ui/tooltip';
import { FiStar, FiBookmark, FiEye } from 'react-icons/fi';
import { getRealiseDate, getGenres, getCollections, getCrewNames } from '../helpers';
import { IMAGE_BASE_URL, FALLBACK_IMAGE_URL } from '~/consts/images';
import { type IError } from '~/types/error';
import styles from '../movie-card.styles';

const MoviePage = () => {
  const { id: movieId } = useParams();
  const { user } = useAppSelector((state) => state.profile);
  const { data: movie, isLoading, error } = useGetMovieQuery(Number(movieId));
  const { data: moviePoster, isLoading: isLoadingPoster } = useGetMoviePosterPathQuery(Number(movieId));

  if (error) {
    return <PageAlert status="error" message={(error as IError).data.detail} />;
  }

  if (isLoading || isLoadingPoster) {
    return <Loader />;
  }

  if (!movie) {
    return <PageAlert status="error" message={'No movie found'} />;
  }

  const collections = getCollections(movie.collections);

  return (
    <Layout>
      <Card.Root css={styles.card}>
        <Image
          src={IMAGE_BASE_URL + moviePoster?.poster_path}
          alt={movie.title}
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.onerror = null;
            target.src = FALLBACK_IMAGE_URL;
          }}
          css={styles.image}
        />

        <Card.Body pt="10px">
          <Stack gap="3">
            <Flex flexDir="row" alignItems="center" gap="4">
              <Heading size="md" flexGrow="1" css={styles.heading}>
                {movie.title}
              </Heading>

              {user.id && (
                <Flex css={styles.icons}>
                  <Tooltip content="Watch later">
                    <IconButton aria-label="Watch later" size="md" variant="ghost">
                      <FiBookmark />
                    </IconButton>
                  </Tooltip>
                  <Tooltip content="Watched">
                    <IconButton aria-label="Watched" size="md" variant="ghost">
                      <FiEye />
                    </IconButton>
                  </Tooltip>
                </Flex>
              )}
            </Flex>

            <Flex flexDir="column" gap="1" py="2">
              <Flex alignItems="center" gap="2">
                <Icon as={FiStar} color="accent.solid" />
                <Text fontSize="md" fontWeight="bold">
                  {movie.vote_average}
                </Text>{' '}
                /
                <Text fontSize="sm" color="neutral.muted">
                  {movie.vote_count} votes
                </Text>
              </Flex>

              {user.id && (
                <>
                  <Text fontSize="sm" color="neutral.muted">
                    Your rating:
                  </Text>
                  <Flex gap="1"></Flex>
                </>
              )}
            </Flex>

            <Text css={styles.text}>
              <span>Release date: </span>
              {getRealiseDate(movie.release_date)}
            </Text>
            <Text css={styles.text}>
              <span>Genres: </span>
              {getGenres(movie.genres)}
            </Text>
            {collections && (
              <Text css={styles.text}>
                <span>Collections: </span>
                {collections}
              </Text>
            )}
            <Text css={styles.text}>
              <span>Cast: </span>
              {getCrewNames(movie.casts)}
            </Text>
            <Text css={styles.text}>
              <span>Director: </span>
              {getCrewNames(movie.directors)}
            </Text>

            <Text css={styles.text}>{movie.overview}</Text>
          </Stack>
        </Card.Body>
      </Card.Root>
    </Layout>
  );
};

export default MoviePage;
