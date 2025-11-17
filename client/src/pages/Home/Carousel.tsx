import type { ReactNode } from 'react';
import { Navigation, FreeMode, Pagination } from 'swiper/modules';
import { Swiper, SwiperSlide } from 'swiper/react';
import MovieCardSmall from './MovieCardSmall';
import MovieCardSmallSkeleton from '~/components/MovieCardSkeleton/MovieCardSmallSkeleton';
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
  const skeletons = Array.from({ length: 10 });
  let content: ReactNode = (
    <NothingFound message="No movies found. Rate movies or add them to your Watch Later or Watched lists to get personalized recommendations" />
  );

  if (isFetching) {
    content = skeletons.map((_, index) => (
      <SwiperSlide key={index} style={{ width: '200px' }}>
        <MovieCardSmallSkeleton />
      </SwiperSlide>
    ));
  } else if (movies && movies.length) {
    content = movies.map((movie) => (
      <SwiperSlide key={movie.id} style={{ width: '200px' }}>
        <MovieCardSmall movie={movie} />
      </SwiperSlide>
    ));
  }

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
      {content}
    </Swiper>
  );
};

export default Carousel;
