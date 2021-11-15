FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /source

# Copy csproj and restore as distinct layers
COPY *.csproj .
RUN dotnet restore

# Copy everything else and build
COPY . .
RUN dotnet publish -c Release -o /app --no-restore

# Build runtime image
FROM mcr.microsoft.com/dotnet/aspnet:6.0
WORKDIR /app
COPY --from=build /app .
EXPOSE 3000
USER 1000
ENTRYPOINT ["dotnet", "user-demo-dotnet.dll"]