import { Box, Flex, Heading, HStack, IconButton, Link, Menu, Icon, Button, Portal } from '@chakra-ui/react';
import { useEffect, useRef } from 'react';
import { FiMenu, FiX } from 'react-icons/fi';
import { Link as ReactRouterLink, NavLink, useNavigate } from 'react-router-dom';
import NavbarAuth from './NavbarAuth';
import styles from './header.styles';

const links = [
  { href: '/movies/best-rating', label: 'Top Rated' },
  { href: '/movies/new', label: 'New Movies' },
  { href: '/movies/popular-now', label: 'Popular Now' },
];

const Header = () => {
  const navigate = useNavigate();

  const header = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const checkScroll = () => {
      if (!header.current) return;

      if (window.scrollY >= 1) {
        header.current.style.boxShadow = '0px 0 10px rgba(0,0,0,.3)';
      } else {
        header.current.style.boxShadow = 'none';
      }
    };

    window.addEventListener('scroll', checkScroll);
    window.addEventListener('resize', checkScroll);

    return () => {
      window.removeEventListener('scroll', checkScroll);
      window.removeEventListener('resize', checkScroll);
    };
  }, []);

  return (
    <Box css={styles.navbar} ref={header}>
      <Flex css={styles.container} h="100%" align="center" justify="space-between">
        <Box css={{ display: { md: 'none' } }}>
          <Menu.Root>
            <Menu.Context>
              {(menu) => (
                <Menu.Trigger asChild>
                  <Button as={IconButton} backgroundColor="pageBgShadow">
                    <Icon boxSize={6} as={menu.open ? FiX : FiMenu} />
                  </Button>
                </Menu.Trigger>
              )}
            </Menu.Context>
            <Portal>
              <Menu.Positioner>
                <Menu.Content backgroundColor="pageBgShadow">
                  {links.map((link) => (
                    <Menu.Item
                      key={link.href}
                      color="primaryText"
                      px={4}
                      py={2}
                      value={link.label}
                      onClick={() => navigate(link.href)}
                    >
                      {link.label}
                    </Menu.Item>
                  ))}
                </Menu.Content>
              </Menu.Positioner>
            </Portal>
          </Menu.Root>
        </Box>
        <Box>
          <ReactRouterLink to="/">
            <Heading size="xl" color="accent.solid" lineHeight="1">
              Movie RS
            </Heading>
          </ReactRouterLink>
        </Box>
        <HStack as="nav" gap={10} align="center" display={{ base: 'none', md: 'flex' }}>
          {links.map((link) => (
            <Link
              asChild
              key={link.label}
              fontWeight="bold"
              color="accent.subtle"
              _hover={{ color: 'accent.emphasized' }}
            >
              <NavLink to={link.href}>{link.label}</NavLink>
            </Link>
          ))}
        </HStack>
        <NavbarAuth />
      </Flex>
    </Box>
  );
};

export default Header;
