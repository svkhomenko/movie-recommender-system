import { toaster } from '~/components/ui/toaster';

type HookType<T> = {
  f: (data: T) => any;
  successMsg?: string;
  successF?: () => void;
};

const useRequestHandler = <T>({ f, successMsg, successF }: HookType<T>) => {
  const handler = async (data: T) => {
    try {
      await f(data).unwrap();
      successMsg &&
        toaster.create({
          description: successMsg,
          type: 'success',
          closable: true,
        });
      successF && successF();
    } catch (error: any) {
      toaster.create({
        description: error.data.detail,
        type: 'error',
        closable: true,
      });
    }
  };

  return { handler };
};

export default useRequestHandler;
