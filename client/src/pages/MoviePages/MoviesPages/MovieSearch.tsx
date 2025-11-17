import { Stack, Input, IconButton } from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import { IoIosSearch } from 'react-icons/io';

export type ISearch = {
  q: string;
};

type IProps = {
  setQ: React.Dispatch<React.SetStateAction<string>>;
};

function MovieSearch({ setQ }: IProps) {
  const { register, getValues } = useForm<ISearch>();

  const updateQ = () => {
    setQ(getValues('q'));
  };

  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    updateQ();
  };

  return (
    <form onSubmit={onSubmit}>
      <Stack direction="row" px="30px" w="100vw">
        <Input
          flexGrow="1"
          id="q"
          placeholder="Movie title, keywords"
          {...register('q', {
            onBlur: updateQ,
          })}
        />
        <IconButton aria-label="Search" size="md" type="submit" flexShrink="0" flexGrow="0">
          <IoIosSearch />
        </IconButton>
      </Stack>
    </form>
  );
}

export default MovieSearch;
