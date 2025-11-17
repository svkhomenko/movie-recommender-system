import { Navigation, FreeMode, Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import MovieCardSmall from './MovieCardSmall';
import NothingFound from '~/components/NothingFound';
import type { IMovieFromList } from '~/types/movie';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

type IProps = {
  movies: IMovieFromList[] | undefined;
  isFetching: boolean;
};

const Carousel = ({ movies, isFetching }: IProps) => {
  return (
    <Swiper
      className="movie-slider"
      slidesPerView="auto"
      spaceBetween={30}
      navigation={true}
      pagination={{
        clickable: true,
      }}
      modules={[FreeMode, Pagination, Navigation]}
    >
      {movies && movies.length ? (
        movies.map((movie) => (
          <SwiperSlide key={movie.id} style={{ width: '200px' }}>
            <MovieCardSmall movie={movie} />
          </SwiperSlide>
        ))
      ) : (
        <NothingFound message="No movies found. Rate movies or add them to your Watch Later or Watched lists to get personalized recommendations" />
      )}
    </Swiper>
  );
};

export default Carousel;
