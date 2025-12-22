import { useMemo, useEffect } from 'react';
import {
  Field,
  Slider,
  Stack,
  Combobox,
  Portal,
  Wrap,
  Badge,
  CloseButton,
  useFilter,
  useListCollection,
} from '@chakra-ui/react';
import { Controller, useForm } from 'react-hook-form';
import { useGetGenresQuery } from '~/store/api/genreSlice';

export type IFilter = {
  years: number[];
  genreIds: string[];
};

type IProps = {
  setYearMin: React.Dispatch<React.SetStateAction<number | null>>;
  setYearMax: React.Dispatch<React.SetStateAction<number | null>>;
  setGenreIds: React.Dispatch<React.SetStateAction<number[]>>;
};

const MovieFilters = ({ setYearMin, setYearMax, setGenreIds }: IProps) => {
  const { data: genresData } = useGetGenresQuery();

  const genres = useMemo(() => {
    if (!genresData || !Array.isArray(genresData)) {
      return [];
    }
    return genresData.map((genre) => ({
      label: genre.name,
      value: genre.id.toString(),
    }));
  }, [genresData]);

  const genreIdToNameMap = useMemo(() => {
    return genres.reduce((acc, genre) => {
      acc[genre.value] = genre.label;
      return acc;
    }, {} as Record<string, string>);
  }, [genres]);

  const currentYear = new Date().getFullYear();
  const { control, getValues } = useForm<IFilter>({ defaultValues: { years: [1870, currentYear], genreIds: [] } });

  const setYears = () => {
    const years = getValues('years');
    setYearMin(years[0]);
    setYearMax(years[1]);
  };

  const { contains } = useFilter({ sensitivity: 'base' });

  const { collection, filter, set } = useListCollection({
    initialItems: genres,
    filter: contains,
  });

  const handleInputChange = (details: Combobox.InputValueChangeDetails) => {
    filter(details.inputValue);
  };

  useEffect(() => {
    set(genres);
  }, [genres]);

  return (
    <form>
      <Stack align="flex-start" gap="4" p="20px 30px" w="100vw" direction={{ base: 'column', lg: 'row' }}>
        <Field.Root flexGrow="1">
          <Controller
            control={control}
            name="genreIds"
            render={({ field }) => {
              const handleRemoveGenre = (genreIdToRemove: string) => {
                const newGenreIds = field.value.filter((id: string) => id !== genreIdToRemove);
                field.onChange(newGenreIds);
                setGenreIds(newGenreIds.map((genreId) => Number(genreId)));
              };

              return (
                <Combobox.Root
                  multiple
                  openOnClick={true}
                  collection={collection}
                  value={field.value || []}
                  onValueChange={({ value }) => {
                    field.onChange(value);
                    setGenreIds(value.map((genreId) => Number(genreId)));
                  }}
                  onInputValueChange={handleInputChange}
                  onInteractOutside={() => field.onBlur()}
                >
                  <Field.Label>
                    Genres:
                    <Wrap gap="2" ml="5px">
                      {(field.value as string[]).map((genreId) => (
                        <Badge key={genreId} size="md" paddingRight="0">
                          {genreIdToNameMap[genreId]}
                          <CloseButton size="sm" w="20px" h="20px" onClick={() => handleRemoveGenre(genreId)} />
                        </Badge>
                      ))}
                    </Wrap>
                  </Field.Label>
                  <Combobox.Control>
                    <Combobox.Input placeholder="Select genre" />
                    <Combobox.IndicatorGroup>
                      <Combobox.ClearTrigger />
                      <Combobox.Trigger />
                    </Combobox.IndicatorGroup>
                  </Combobox.Control>

                  <Portal>
                    <Combobox.Positioner backgroundColor="pageBgShadow">
                      <Combobox.Content>
                        <Combobox.Empty>No genres found</Combobox.Empty>
                        {collection.items.map((item) => (
                          <Combobox.Item key={item.value} item={item}>
                            {item.label}
                            <Combobox.ItemIndicator />
                          </Combobox.Item>
                        ))}
                      </Combobox.Content>
                    </Combobox.Positioner>
                  </Portal>
                </Combobox.Root>
              );
            }}
          />
        </Field.Root>

        <Controller
          name="years"
          control={control}
          render={({ field }) => (
            <Field.Root width="300px" flexShrink="0" flexGrow="0">
              <Slider.Root
                width="300px"
                name={field.name}
                value={field.value}
                min={1870}
                max={currentYear}
                onValueChange={({ value }) => {
                  field.onChange(value);
                }}
                onFocusChange={({ focusedIndex }) => {
                  if (focusedIndex !== -1) return;
                  field.onBlur();
                }}
                onValueChangeEnd={setYears}
              >
                <Slider.Label pb="10px">
                  Years: {field.value[0]} - {field.value[1]}
                </Slider.Label>
                <Slider.Control>
                  <Slider.Track bg="cardBg">
                    <Slider.Range />
                  </Slider.Track>
                  <Slider.Thumbs />
                </Slider.Control>
              </Slider.Root>
            </Field.Root>
          )}
        />
      </Stack>
    </form>
  );
};

export default MovieFilters;
