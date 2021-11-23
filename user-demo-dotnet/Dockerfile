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

ENV PORT 3000
ENV ASPNETCORE_URLS "http://0.0.0.0:${PORT}"
EXPOSE ${PORT}

USER 1000
ENTRYPOINT ["dotnet", "user-demo-dotnet.dll"]
