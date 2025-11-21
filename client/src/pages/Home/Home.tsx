import MoviesCarousel from './MoviesCarousel';
import { useAppSelector } from '~/hooks/useAppSelector';
import { MOVIES_RESULT_TYPES } from '~/consts/movies';

const carouselTypes = [
  { href: '/movies/best-rating', type: MOVIES_RESULT_TYPES.BEST_RATING },
  { href: '/movies/new', type: MOVIES_RESULT_TYPES.NEW },
  { href: '/movies/popular-now', type: MOVIES_RESULT_TYPES.POPULAR_NOW },
];

const carouselUserTypes = [
  { href: '/movies/recommendations', type: MOVIES_RESULT_TYPES.RECOMMENDATIONS },
  { href: '/movies/continue-watching', type: MOVIES_RESULT_TYPES.CONTINUE_WATCHING },
];

const Home = () => {
  const { user } = useAppSelector((state) => state.profile);

  return (
    <>
      {user.id &&
        carouselUserTypes.map((type) => <MoviesCarousel key={type.href} resultType={type.type} href={type.href} />)}
      {carouselTypes.map((type) => (
        <MoviesCarousel key={type.href} resultType={type.type} href={type.href} />
      ))}
    </>
  );
};

export default Home;
