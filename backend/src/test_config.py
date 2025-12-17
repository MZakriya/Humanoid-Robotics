"""
Test script for environment variable configuration.
This script tests that the configuration module properly loads environment variables.
"""
import os
from config import Config, config


def test_config_loading():
    """
    Test that configuration is properly loaded from environment variables.
    """
    print("Testing environment variable configuration...")

    # Test FastAPI settings
    print(f"FASTAPI_HOST: {config.FASTAPI_HOST}")
    print(f"FASTAPI_PORT: {config.FASTAPI_PORT}")
    print(f"API_SECRET_KEY: {'SET' if config.API_SECRET_KEY and config.API_SECRET_KEY != 'your-secret-key-here' else 'NOT SET OR DEFAULT'}")

    # Test Qdrant settings
    print(f"QDRANT_URL: {config.QDRANT_URL if config.QDRANT_URL else 'NOT SET'}")
    print(f"QDRANT_API_KEY: {'SET' if config.QDRANT_API_KEY else 'NOT SET'}")
    print(f"QDRANT_COLLECTION_NAME: {config.QDRANT_COLLECTION_NAME}")

    # Test OpenAI settings
    print(f"OPENAI_API_KEY: {'SET' if config.OPENAI_API_KEY else 'NOT SET'}")
    print(f"EMBEDDING_MODEL_NAME: {config.EMBEDDING_MODEL_NAME}")

    # Test Neon Postgres settings
    print(f"NEON_PG_URL: {config.NEON_PG_URL if config.NEON_PG_URL else 'NOT SET'}")

    # Test Better Auth settings
    print(f"BETTER_AUTH_CLIENT_ID: {'SET' if config.BETTER_AUTH_CLIENT_ID else 'NOT SET'}")
    print(f"BETTER_AUTH_SECRET: {'SET' if config.BETTER_AUTH_SECRET else 'NOT SET'}")

    # Test development settings
    print(f"DEBUG: {config.DEBUG}")
    print(f"LOG_LEVEL: {config.LOG_LEVEL}")

    # Test application settings
    print(f"MAX_CONTENT_LENGTH: {config.MAX_CONTENT_LENGTH}")

    # Validate configuration
    is_valid = Config.validate_config()
    print(f"\nConfiguration validation: {'PASSED' if is_valid else 'FAILED'}")

    if not is_valid:
        print("Note: Some variables may have default values. This is expected in development.")

    return is_valid


def test_qdrant_config():
    """
    Test Qdrant configuration dictionary
    """
    qdrant_config = config.get_qdrant_config()
    print(f"\nQdrant Config: {qdrant_config}")
    return True


def test_openai_config():
    """
    Test OpenAI configuration dictionary
    """
    openai_config = config.get_openai_config()
    print(f"OpenAI Config: {openai_config}")
    return True


def test_neon_config():
    """
    Test Neon configuration dictionary
    """
    neon_config = config.get_neon_config()
    print(f"Neon Config: {neon_config}")
    return True


def test_auth_config():
    """
    Test Auth configuration dictionary
    """
    auth_config = config.get_auth_config()
    print(f"Auth Config: {auth_config}")
    return True


def main():
    """
    Main function to run all configuration tests.
    """
    print("="*60)
    print("ENVIRONMENT VARIABLE CONFIGURATION TEST")
    print("="*60)

    # Run all tests
    tests = [
        ("Configuration Loading", test_config_loading),
        ("Qdrant Config", test_qdrant_config),
        ("OpenAI Config", test_openai_config),
        ("Neon Config", test_neon_config),
        ("Auth Config", test_auth_config),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"✓ {test_name}: {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            print(f"✗ {test_name}: FAILED - {str(e)}")
            results.append((test_name, False))

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")

    all_passed = all(result for _, result in results)
    print(f"\nOverall: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())