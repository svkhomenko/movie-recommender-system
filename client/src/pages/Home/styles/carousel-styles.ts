import { type SystemStyleObject } from '@chakra-ui/react';

type StylesType = {
  box: SystemStyleObject;
};

export const styles: StylesType = {
  box: {
    '& .movie-slider': {
      '--swiper-theme-color': '#f9bc85',
    },
  },
};

export default styles;
