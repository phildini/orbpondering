# Orbpondering - Enhanced Publishing Workflow

## Workflow Design Philosophy

This workflow follows the same patterns as `django-stagedoor` but adapted for orbpondering's specific needs:

### Key Features Implemented

1. **Trigger-Based Publishing**:
   - Automatically triggered by git tag pushes (`v*` pattern)
   - Manual override via workflow dispatch
   - Consistent with semantic versioning practices

2. **Version Management**:
   - Auto-detects version from git tag (e.g., `v1.2.3`)
   - Manual override when needed
   - Falls back to default `v0.1.0` if no tag detected

3. **Reliable Build Process**:
   - Uses `hatch` for consistent packaging
   - Proper Python environment setup
   - Caching for faster builds

4. **Secure Publishing**:
   - Uses GitHub Trusted Publisher (OIDC authentication)
   - `skip-existing: true` to prevent duplicate uploads
   - Environment isolation for publishing

## Workflow Behavior

### 1. Automatic Release (Tag Push)
When you push a tag:
```bash
git tag v1.2.3
git push origin v1.2.3
```
- Workflow triggers automatically
- Version detected from tag: `v1.2.3`
- Package built with version `1.2.3`
- Published to PyPI

### 2. Manual Release (Workflow Dispatch)
1. Go to GitHub Actions
2. Run "Publish Package" workflow manually
3. Optionally enter version (e.g., `1.2.4`)
4. Workflow builds and publishes with specified version

### 3. Fallback Behavior
If no git tag and no manual version provided:
- Uses default version `v0.1.0`
- Prevents publishing with malformed versions

## Implementation Details

The workflow:
1. **Checks out code** with full history
2. **Sets up Python 3.12 environment** with dependency caching
3. **Installs hatch** for package management
4. **Extracts version** from git tag or manual input
5. **Sets package version** using hatch
6. **Builds distributable** with proper version
7. **Publishes to PyPI** via Trusted Publisher

## Verification Commands

```bash
# Test version detection
git describe --tags --exact-match 2>/dev/null || echo "No exact tag"

# Test hatch version setting
hatch version v1.2.3

# Test build process
hatch build
```

## Maintenance Notes

1. **Version Convention**: Always use `vMAJOR.MINOR.PATCH` format (e.g., `v1.2.3`)
2. **Release Process**: 
   - Create tag: `git tag v1.2.3`
   - Push tag: `git push origin v1.2.3`
   - GitHub Actions handles publishing automatically
3. **Manual Override**: Useful for hotfixes or testing pre-releases