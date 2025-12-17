import React, { useState, useEffect } from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import { useLocation } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import { useThemeConfig } from '@docusaurus/theme-common';
import { ThemeClassNames } from '@docusaurus/utils';
import useLockBodyScroll from '@docusaurus/useLockBodyScroll';
import useWindowSize from '@docusaurus/useWindowSize';
import NavbarItem from '@theme/NavbarItem';
import Logo from '@theme/Logo';
import SearchBar from '@theme/SearchBar';
import IconMenu from '@theme/IconMenu';
import { translate } from '@docusaurus/Translate';

import './styles.css';

// Placeholder for session management - in real implementation, this would use Better Auth hooks
const useAuth = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Simulate checking for authenticated user
  useEffect(() => {
    const checkAuth = async () => {
      try {
        // In a real implementation, this would call Better Auth's session API
        const response = await fetch('/api/auth/session');
        if (response.ok) {
          const userData = await response.json();
          setUser(userData);
        }
      } catch (error) {
        console.error('Error checking auth status:', error);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = () => {
    // In a real implementation, this would redirect to Better Auth login
    window.location.href = '/api/auth/login';
  };

  const logout = async () => {
    try {
      // In a real implementation, this would call Better Auth's logout API
      await fetch('/api/auth/logout', { method: 'POST' });
      setUser(null);
      // Optionally redirect to home page
      window.location.href = '/';
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  return { user, loading, login, logout };
};

const NavbarContentLayout = ({ left, right }) => (
  <div className="navbar__inner">
    <div className="navbar__items">{left}</div>
    <div className="navbar__items navbar__items--right">{right}</div>
  </div>
);

function useNavbarContent() {
  const location = useLocation();
  const themeConfig = useThemeConfig();
  const { navbar: { items, hideOnScroll, title, hideTitle }, colorMode } = themeConfig;
  const logo = themeConfig.navbar.logo;
  const [sidebarShown, setSidebarShown] = useState(false);
  const [isSearchBarExpanded, setIsSearchBarExpanded] = useState(false);

  useLockBodyScroll(sidebarShown);

  const { user, loading, login, logout } = useAuth();

  const itemsToShow = items ?? [];

  const showLogo = logo != null && (location.pathname === '/' || logo.target === '_self');
  const showTitle = !hideTitle && title;

  const navbarHideable = hideOnScroll;
  const mobileSidebarToggleItem = itemsToShow.find((item) => item.type === 'toggle');
  const navbarItems = itemsToShow
    .filter((item) => item.position !== 'right')
    .concat(mobileSidebarToggleItem ? [] : [{ type: 'toggle' }]);
  const navbarItemsRight = itemsToShow.filter((item) => item.position === 'right');

  return {
    navbarHideable,
    sidebarShown,
    setSidebarShown,
    isSearchBarExpanded,
    setIsSearchBarExpanded,
    showLogo,
    showTitle,
    navbarItems,
    navbarItemsRight,
    user,
    loading,
    login,
    logout
  };
}

function NavbarContent() {
  const {
    sidebarShown,
    setSidebarShown,
    isSearchBarExpanded,
    setIsSearchBarExpanded,
    showLogo,
    showTitle,
    navbarItems,
    navbarItemsRight,
    user,
    loading,
    login,
    logout
  } = useNavbarContent();

  // Center the logo/title in the middle
  const itemsLeft = (
    <>
      {showLogo && <Logo className="navbar__logo" />}
      {showTitle && <Link className="navbar__title" to={useBaseUrl('/')}>{title}</Link>}
      {navbarItems.map((item, i) => (
        <NavbarItem {...item} key={i} />
      ))}
    </>
  );

  const itemsRight = (
    <>
      {navbarItemsRight.map((item, i) => (
        <NavbarItem {...item} key={i} />
      ))}
      <NavbarItem className="navbar__auth-buttons">
        {loading ? (
          <span>Loading...</span>
        ) : user ? (
          <div className="navbar__user-menu">
            <span className="navbar__user-name">Hi, {user.name || user.email}</span>
            <button className="navbar__logout-btn" onClick={logout}>
              Logout
            </button>
          </div>
        ) : (
          <button className="navbar__login-btn" onClick={login}>
            Login
          </button>
        )}
      </NavbarItem>
      {!isSearchBarExpanded && <SearchBar />}
    </>
  );

  return (
    <NavbarContentLayout left={itemsLeft} right={itemsRight} />
  );
}

function NavbarMinimal() {
  const {
    sidebarShown,
    setSidebarShown,
    isSearchBarExpanded,
    setIsSearchBarExpanded,
    showLogo,
    showTitle,
    navbarItems,
    navbarItemsRight,
    user,
    loading,
    login,
    logout
  } = useNavbarContent();

  // Create a centered navbar with logo/title in the center
  return (
    <div className="navbar__inner--centered">
      <div className="navbar__items--left">
        {navbarItems.map((item, i) => (
          <NavbarItem {...item} key={i} />
        ))}
      </div>

      <div className="navbar__logo-title">
        {showLogo && <Logo className="navbar__logo--center" />}
        {showTitle && <Link className="navbar__title--center" to={useBaseUrl('/')}>{title}</Link>}
      </div>

      <div className="navbar__items--right">
        {navbarItemsRight.map((item, i) => (
          <NavbarItem {...item} key={i} />
        ))}
        <NavbarItem className="navbar__auth-buttons">
          {loading ? (
            <span>Loading...</span>
          ) : user ? (
            <div className="navbar__user-menu">
              <span className="navbar__user-name">Hi, {user.name || user.email}</span>
              <button className="navbar__logout-btn" onClick={logout}>
                Logout
              </button>
            </div>
          ) : (
            <button className="navbar__login-btn" onClick={login}>
              Login
            </button>
          )}
        </NavbarItem>
        {!isSearchBarExpanded && <SearchBar />}
      </div>
    </div>
  );
}

function Navbar() {
  const { sidebarShown, setSidebarShown, navbarHideable } = useNavbarContent();
  const location = useLocation();
  const windowSize = useWindowSize();

  useEffect(() => {
    if (windowSize === 'desktop') {
      setSidebarShown(false);
    }
  }, [windowSize, setSidebarShown]);

  return (
    <nav
      className={clsx(
        'navbar',
        'navbar--fixed-top',
        navbarHideable && 'navbar--hideable',
        sidebarShown && 'navbar-sidebar--show',
        ThemeClassNames.navbar,
      )}
      aria-label={translate({ id: 'theme.NavBar.navAriaLabel', message: 'Main' })}>
      <div className="navbar__inner">
        <div className="navbar__items">
          <button
            aria-label={translate({
              id: 'theme.navbar.mobileSidebarToggleAriaLabel',
              message: 'Toggle navigation bar',
            })}
            className="navbar__toggle clean-btn"
            type="button"
            onClick={() => setSidebarShown(!sidebarShown)}>
            <IconMenu />
          </button>
        </div>
        {/* Use the centered navbar layout */}
        <NavbarMinimal />
      </div>
      <div className="navbar-sidebar__items">
        <NavbarContent />
      </div>
      <div className="navbar-sidebar__backdrop" role="presentation" onClick={() => setSidebarShown(false)} />
    </nav>
  );
}

export default Navbar;