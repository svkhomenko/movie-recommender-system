import { Field, RatingGroup, Flex, IconButton } from '@chakra-ui/react';
import { zodResolver } from '@hookform/resolvers/zod';
import { Controller, useForm } from 'react-hook-form';
import useRequestHandler from '~/hooks/useRequestHandler';
import { useCreaterMovieRatingMutation, useDeleteMovieRatingMutation } from '~/store/api/movieSlice';
import { Tooltip } from '~/components/ui/tooltip';
import { TiDeleteOutline } from 'react-icons/ti';
import { createRatingSchema, type ICreateRating } from '~/validation/movies';
import { type IMovie } from '~/types/movie';

type IPropsDeleteRatingButton = {
  movie: IMovie;
  onRatingDeleted: () => void;
};

const DeleteRatingButton = ({ movie, onRatingDeleted }: IPropsDeleteRatingButton) => {
  const [deleteMovieRating, { isLoading }] = useDeleteMovieRatingMutation();

  const { handler: deleteMovieRatingHandler } = useRequestHandler<number>({
    f: deleteMovieRating,
    successMsg: 'Rating was successfully deleted.',
    successF: onRatingDeleted,
  });

  return (
    <Tooltip content="Delete rating">
      <IconButton
        aria-label="Delete rating"
        size="md"
        variant="ghost"
        onClick={() => deleteMovieRatingHandler(movie.id)}
        loading={isLoading}
      >
        <TiDeleteOutline />
      </IconButton>
    </Tooltip>
  );
};

type IPropsRatingButton = {
  movie: IMovie;
};

const RatingButton = ({ movie }: IPropsRatingButton) => {
  const [createMovieRating] = useCreaterMovieRatingMutation();

  const { handler: createMovieRatingHandler } = useRequestHandler<ICreateRating & Pick<IMovie, 'id'>>({
    f: createMovieRating,
    successMsg: 'Movie was successfully rated.',
  });

  const {
    handleSubmit,
    formState: { errors },
    setValue,
    control,
    reset,
  } = useForm<ICreateRating>({
    resolver: zodResolver(createRatingSchema),
    defaultValues: { rating: movie.rating },
  });

  const onSubmit = async (data: ICreateRating) => {
    await createMovieRatingHandler({ ...data, id: movie.id });
  };

  const handleRatingChange = async (value: number) => {
    setValue('rating', value, { shouldValidate: true, shouldDirty: true });
    await handleSubmit(onSubmit)();
  };

  return (
    <form>
      <Field.Root invalid={!!errors.rating}>
        <Flex alignItems="center" gap="3" height="40px">
          <Field.Label color="neutral.muted" fontSize="md">
            Your rating:
          </Field.Label>
          <Controller
            control={control}
            name="rating"
            render={({ field }) => (
              <RatingGroup.Root
                count={10}
                name={field.name}
                value={field.value}
                onValueChange={({ value }) => {
                  handleRatingChange(value);
                }}
              >
                <RatingGroup.HiddenInput />
                <RatingGroup.Control />
              </RatingGroup.Root>
            )}
          />
          {movie.rating && <DeleteRatingButton movie={movie} onRatingDeleted={() => reset({ rating: undefined })} />}
        </Flex>
        <Field.ErrorText>{errors.rating?.message}</Field.ErrorText>
      </Field.Root>
    </form>
  );
};

export default RatingButton;
